class Supplier:
    """A company that supplies products to the store.

    Association: a Product knows its Supplier, but neither owns the other,
    so both can exist on their own
    """

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:

        self.__supplier_id = supplier_id
        self.__name = name
        self.__contact_email = contact_email

    @property
    def supplier_id(self) -> str:
        return self.__supplier_id  

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact_email(self) -> str:
        return self.__contact_email


    def display_information(self) -> None:
        print(f"ID: {self.__supplier_id} | Name: {self.__name} | Contact Email: {self.__contact_email}")
