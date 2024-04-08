from . import models, schemas
from sqlalchemy.orm import Session
from role.models import Role_model
#get all accounts
def get_all_role(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Role_model).offset(skip).limit(limit).all()

#get by id
def get_by_role_id(db: Session, role_id : int):
    #select * from account WHERE id='1'
    return db.query(models.Role_model).filter(models.Role_model.id == role_id).first()

#get by name
def get_by_role_name(db: Session, role_name: str):
    #select * from account WHERE name='1'
    return db.query(models.Role_model).filter(models.Role_model.role == role_name).first()

#create account
def create_role(db: Session, role : schemas.RoleCreate):
    new_role = models.Role_model(**role.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

#update account
def update_role(db: Session, role_id: int, role: schemas.RoleUpdate):
    #retrieve account
    existing_role = db.query(Role_model).filter(Role_model.id == role_id)
    if not existing_role.first():
          return ValueError(f"Account id {role_id} not found")
    existing_role.update(role.dict())
    db.commit()
    return existing_role

#delete account
def delete_role(db: Session, role_id : int):
    existing_role = db.query(models.Role_model).filter(models.Role_model.id == role_id)
    if not existing_role.first():
        raise ValueError(f"Account id {role_id} not found")
    existing_role.delete()
    db.commit()
    


