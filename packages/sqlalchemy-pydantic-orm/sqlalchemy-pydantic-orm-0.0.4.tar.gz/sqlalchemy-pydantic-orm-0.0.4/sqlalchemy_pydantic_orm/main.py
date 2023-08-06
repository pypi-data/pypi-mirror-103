"""TODO: Module documentation"""

from abc import abstractmethod
from typing import Type, Any

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta

SUPPORTED_ITERABLES = (list, tuple, set)  # Could be extended


class ORMBaseSchema(BaseModel):
    """TODO: Class documentation"""

    class Config:
        """Pydantic's default config class except with orm_mode set to True."""
        orm_mode = True

    @property
    @abstractmethod
    def _orm_model(self) -> Type[DeclarativeMeta]:
        """The corresponding SQLAlchemy model class

        This is an abstract property, which means that inherited classes are
        forced to define this as class variable (or property), when missing it
        throws an error.

        This variable/property has a leading underscore and can only be
        assigned as PrivateAttr (Pydantic). This is because a Pydantic schema
        iterates over it's own fields and would otherwise cause problems when
        encountering this variable/property.

        Returns:
            A SQLAlchemy model (indirectly) inherited from DeclarativeMeta
        """
        pass

    def __init__(self, **data: Any):
        """Init used for validation and throwing errors where needed.

        Pydantic catches all ValueError's in initialization, and then outputs
        the error message in a easy to read format with the specific class
        name displayed.
        Every error is given the "sqlalchemy-pydantic-orm" identifier to
        distinguish between Pydantic's or SQLAlchemy's own errors
        and those of this package.

        For performance its better to execute the `super().__init__()` as late
        as possible, only the _orm_model check requires it to work properly.

        Args:
            **data (Any):
                The fields and values to be validated.

        Raises:
            ValueError:
                When orm_mode is set to false /
                When the provided _orm_model is invalid
        """
        if not hasattr(config := self.Config, "orm_mode"):
            # Overwriting when not defined
            config.orm_mode = True
        elif not config.orm_mode:
            # Throws an error instead of overwriting to avoid confusion
            raise ValueError(
                "sqlalchemy-pydantic-orm: "
                "When adding your own 'Config' class, "
                "make sure you set 'orm_mode' to 'true'"
            )

        super().__init__(**data)

        if type(self._orm_model) != DeclarativeMeta:
            raise ValueError(
                "sqlalchemy-pydantic-orm: "
                "Provided orm_model is not a valid SQLAlchemy model, "
                "make sure it inherits the declarative base"
            )
        elif "_orm_model" not in self.__private_attributes__:
            raise ValueError(
                "sqlalchemy-pydantic-orm: "
                "Provided orm_model is not wrapped in a pydantic PrivateAttr"
            )

    def orm_create(self, **extra_fields: Any) -> DeclarativeMeta:
        """Method to convert a (nested) pydantic schema to a SQLAlchemy model.

        Using the validated fields in this class, together with the defined
        _orm_model, this recursive methods creates a (nested) SQLAlchemy model.

        Args:
            extra_fields (Any):
                Extra fields (keyword arguments) not defined in the pydantic
                schema used by the top level ORM model. The fields in the
                schema itself have priority.

                Usage example:
                    When using an API like FastAPI or Flask, you often get
                    the data as body while getting the id (foreign key) as
                    path parameter. This argument lets you add such an id from
                    a separate source.

        Returns:
            A SQLAlchemy model instance, that still has to be added to the db.

        Raises:
            TypeError:
                When a list is not fully consisted of other ORM schemas.
        """
        current_level_fields = {}
        for field in self.__fields_set__:
            field_name = self.__fields__[field].alias
            value = getattr(self, field)
            if isinstance(value, ORMBaseSchema):  # One-to-one
                current_level_fields[field_name] = value.orm_create()

            elif isinstance(value, SUPPORTED_ITERABLES):  # One-to-many
                models = []
                for schema in value:
                    if not isinstance(schema, ORMBaseSchema):
                        raise TypeError(
                            "Lists should only contain other schemas "
                            f"inherited from '{ORMBaseSchema.__name__}' "
                            "(sqlalchemy-pydantic-orm)"
                        )
                    models.append(schema.orm_create())
                current_level_fields[field_name] = models

            else:  # value without relation
                current_level_fields[field_name] = value

        return self._orm_model(**extra_fields, **current_level_fields)

    def orm_update(self, db: Session, db_model: DeclarativeMeta) -> None:
        """Method to update a (nested) orm structure.

        This method recursively updates an orm model with it's relationships.

        In one-to-many relationships, each provided item without an id gets
        added as new item with the `orm_create()` method. When a valid id is
        provided it updates the item with the `orm_update()` method. It also
        keep track of the parsed database items, and afterwards deletes any
        unparsed item.

        Args:
            db (Session):
                Database session used for `.add()` and `.delete()`.
            db_model (DeclarativeMeta):
                The ORM model to be updated.

        Returns:
            Nothing, everything gets done in the provided db_model

        Raises:
            TypeError:
                When a list is not fully consisted of other ORM schemas.
            ValueError:
                When the provided db_model is not valid /
                When a given id is not found in the database
        """
        if not isinstance(db_model, self._orm_model):
            raise ValueError(
                f"Provided db_model '{db_model}' is not an instance of the "
                f"defined _orm_model '{self._orm_model.__name__}' "
                "(sqlalchemy-pydantic-orm)"
            )
        for field in self.__fields_set__:
            field_name = self.__fields__[field].alias
            db_value = getattr(db_model, field_name)
            update_value = getattr(self, field)
            if isinstance(update_value, ORMBaseSchema):  # One-to-one
                if db_value:
                    update_value.orm_update(db, db_value)
                else:
                    setattr(db_model, field_name, update_value.orm_create())

            elif isinstance(update_value, SUPPORTED_ITERABLES):  # One-to-many
                parsed_items = set()
                for schema in update_value:
                    if not isinstance(schema, ORMBaseSchema):
                        raise TypeError(
                            "Lists should only contain other schemas "
                            f"inherited from '{ORMBaseSchema.__name__}' "
                            "(sqlalchemy-pydantic-orm)"
                        )
                    if item_id := getattr(schema, "id", None):
                        try:
                            db_item = next(
                                item for item in db_value if item.id == item_id
                            )
                        except StopIteration:
                            raise ValueError(
                                f"Provied id '{item_id}' "
                                f"for field '{field_name}' "
                                "can't be found in the database "
                                "(sqlalchemy-pydantic-orm)"
                            ) from None  # removes unnecessary traceback

                        schema.orm_update(db, db_item)
                        parsed_items.add(db_item)
                    else:
                        new_item = schema.orm_create()
                        parsed_items.add(new_item)
                        db_value.append(new_item)

                for db_item in db_value:
                    if db_item not in parsed_items:
                        db.delete(db_item)
            else:
                setattr(db_model, field_name, update_value)

    def to_orm(self, db: Session, **extra_fields: Any) -> DeclarativeMeta:
        """Method that combines the functionality of orm_create & orm_update.

        This method is a wrapper around the other two methods. When no id is
        provided, it creates a new model with orm_create, and when an id ís
        provided, it retrieves and updates that model.

        In contrary to the orm_create function on its own, this function does
        add the newly created model to the database. So after the this method
        has been executed you only need to call `db.commit()` after.

        Args:
            db (Session):
            **extra_fields (Any):

        Returns:
            A SQLAlchemy model instance, which is either queried and updated,
                or newly created

        Raises:
            ValueError:
                When the provided id is not found in the database
        """
        id_ = getattr(self, "id", None)
        if not id_ and "id" in extra_fields:  # Pydantic field has priority
            id_ = extra_fields["id"]
        if id_:
            db_model = db.query(self._orm_model).get(id_)
            if not db_model:
                raise ValueError(
                    f"Provied id '{id_}' "
                    f"for table '{self._orm_model.__tablename__}' "  # noqa
                    "can't be found in the database "
                    "(sqlalchemy-pydantic-orm)"
                )
            self.orm_update(db, db_model)
        else:
            db_model = self.orm_create(**extra_fields)
            db.add(db_model)

        return db_model

# class _ORMBaseConfig(BaseConfig):
#     orm_mode = True
#
#
# def sqlalchemy_to_pydantic(
#         db_model: Type, *,
#         exclude: Container[str] = None,
# ) -> Type[BaseModel]:
#     if exclude is None:
#         exclude = ()
#
#     mapper = inspect(db_model)
#     fields = {}
#     for attr in mapper.attrs:
#         if isinstance(attr, ColumnProperty):
#             if attr.columns:
#                 name = attr.key
#                 if name in exclude:
#                     continue
#                 column = attr.columns[0]
#                 python_type: Optional[type] = None
#                 if hasattr(column.type, "impl"):
#                     if hasattr(column.type.impl, "python_type"):
#                         python_type = column.type.impl.python_type
#                 elif hasattr(column.type, "python_type"):
#                     python_type = column.type.python_type
#                 if not python_type:
#                     raise ValueError(
#                         f"Could not infer python_type for {column} "
#                         "(sqlalchemy-pydantic-orm)"
#                     )
#                 default = None
#                 if column.default is None and not column.nullable:
#                     default = ...
#
#                 fields[name] = (python_type, default)
#
#     fields["_orm_model"] = PrivateAttr(db_model)
#     pydantic_model = create_model(
#         db_model.__name__,
#         __base__=ORMBaseSchema,  # Cant go together with __config__
#         **fields
#     )
#     return pydantic_model
