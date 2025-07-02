from models import Company, Staff
from sqlalchemy.orm import sessionmaker
from connection import engine

Session = sessionmaker(bind=engine)

def _serialize(company):
    data = {
        "id": company.id,
        "name": company.name,
        "location": company.location,
    }
    return data

def _serialize_staff(staff):
    return {
        "id": staff.id,
        "name": staff.name,
        "role": staff.role,
        "salary": staff.salary,
        "email": staff.email,
        "phoneNumber": staff.phoneNumber,
        "company_id": staff.company_id
    }

# Company CRUD

def create_company(name, location):
    session = Session()
    try:
        exists = session.query(Company).filter(Company.name == name).first()
        if exists:
            raise Exception("Company already exists")
        new_company = Company(
            name=name, 
            location=location)
        session.add(new_company)
        session.commit()
        return _serialize(new_company)
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


def read_companies():
    session = Session()
    try:
        return session.query(Company).all()
    finally:
        session.close()

        
def get_company(identifier):
    session = Session()
    try:
        if isinstance(identifier, int):
            company = session.query(Company).get(identifier)
        else:
            company = session.query(Company).filter(Company.name == identifier).first()

        if not company:
            raise Exception("Company not found")

        return {
            "id": company.id,
            "name": company.name,
            "location": company.location
        }

    finally:
        session.close()


def update_company(identifier, name=None, location=None):
    session = Session()
    try:
        if isinstance(identifier, int):
            company = session.query(Company).get(identifier)
        else:
            company = session.query(Company).filter(Company.name == identifier).first()
        if not company:
            raise Exception("Company not found")
        if name:
            company.name = name
        if location:
            company.location = location
        session.commit()
        return _serialize(company)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_company(identifier):
    session = Session()
    try:
        if isinstance(identifier, int):
            company = session.query(Company).get(identifier)
        else:
            company = session.query(Company).filter(Company.name == identifier).first()
        if not company:
            raise Exception("Company not found")
        session.delete(company)
        session.commit()
        return {
            "id": company.id,
            "name": company.name,
            "location": company.location
        }
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()



# Staff CRUD

def create_staff(name, role, company_id, salary, email, phoneNumber):
    session = Session()
    try:
        staff = session.query(Staff).filter(Staff.email == email).first()
        if staff:
            raise Exception("Staff already exists")
        new_staff = Staff(
            name=name,
            role=role,
            company_id=company_id,
            salary=salary,
            email=email,
            phoneNumber=phoneNumber
        )
        session.add(new_staff)
        session.commit()
        return _serialize_staff(new_staff)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def read_staff():
    session = Session()
    try:
        return session.query(Staff).all()
    finally:
        session.close()


def get_staff(identifier):
    session = Session()
    try:
        if isinstance(identifier, int):
            staff = session.query(Staff).get(identifier)
        else:
            staff = session.query(Staff).filter(Staff.email == identifier).first()
        if not staff:
            raise Exception("Staff member not found")
        return {
        "id": staff.id,
        "name": staff.name,
        "role": staff.role,
        "salary": staff.salary,
        "email": staff.email,
        "phoneNumber": staff.phoneNumber,
        "company_id": staff.company_id
    }
    finally:
        session.close()


def update_staff(identifier, name=None, role=None, salary=None, email=None, phoneNumber=None):
    session = Session()
    try:
        if isinstance(identifier, int):
            staff = session.query(Staff).get(identifier)
        else:
            staff = session.query(Staff).filter(Staff.email == identifier).first()
        if not staff:
            raise Exception("Staff member not found")
        if name:
            staff.name = name
        if role:
            staff.role = role
        if salary is not None:
            staff.salary = salary
        if email is not None:
            staff.email = email
        if phoneNumber is not None:
            staff.phoneNumber = phoneNumber
        session.commit()
        return _serialize(staff)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_staff(identifier):
    session = Session()
    try:
        if isinstance(identifier, int):
            staff = session.query(Staff).get(identifier)
        else:
            staff = session.query(Staff).filter(Staff.email == identifier).first()
        if not staff:
            raise Exception("Staff member not found")
        session.delete(staff)
        session.commit()
        return {
            "id": staff.id,
            "name": staff.name,
            "role": staff.role
        }
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_staff_by_company_name(identifier):
    session = Session()
    try:
        if isinstance(identifier, int):
            company = session.query(Company).get(identifier)
        else:
            company = session.query(Company).filter(Company.name == identifier).first()
        if not company:
            raise Exception("Company not found")
        staff_list = session.query(Staff).filter(Staff.company_id == company.id).all()
        return [
            {
                "id": staff.id,
                "name": staff.name,
                "role": staff.role,
                "salary": staff.salary,
                "email": staff.email,
                "phoneNumber": staff.phoneNumber,
                "company_id": staff.company_id
            }
            for staff in staff_list
        ]
    finally:
        session.close()


def get_staff_and_company(identifier):
    session = Session()
    try:
        # Find staff by id or email
        if isinstance(identifier, int):
            staff = session.query(Staff).get(identifier)
        else:
            staff = session.query(Staff).filter(Staff.email == identifier).first()
        if not staff:
            raise Exception("Staff member not found")
        # Find the company
        company = session.query(Company).get(staff.company_id)
        if not company:
            raise Exception("Company not found for this staff member")
        staff_info = {
            "id": staff.id,
            "name": staff.name,
            "role": staff.role,
            "salary": staff.salary,
            "email": staff.email,
            "phoneNumber": staff.phoneNumber,
            "company_id": staff.company_id
        }
        company_info = {
            "id": company.id,
            "name": company.name,
            "location": company.location
        }
        return {
            "staff": staff_info,
            "company": company_info
        }
    finally:
        session.close()
