from fastapi import APIRouter
from model.person import Person
from service import person_service
from model.filterperson import FilterPerson

router = APIRouter(prefix="/person")

@router.post("/filter/")
def get_by_filters_json(filters: FilterPerson):
    return person_service.get_persons_by_conditions(filters.code, filters.typedoc, filters.gender)

@router.post("/")
def create(person: Person):
    return person_service.create_person(person)

@router.get("/")
def get_all():
    return person_service.list_persons()

@router.get("/location/{code}")
def get_by_location(code: str):
    return person_service.get_persons_by_location(code)

#@router.get("/filter/")
#def get_by_filters(code: str, typedoc: str, gender: str):
#    return person_service.get_persons_by_conditions(code, typedoc, gender)

@router.get("/adults/daughters")
def get_parents():
    return person_service.get_parents_with_adult_daughters()

@router.put("/{person_id}")
def update(person_id: int, person: Person):
    return person_service.update_person(person_id, person)

@router.delete("/{person_id}")
def delete(person_id: int):
    return person_service.delete_person(person_id)


