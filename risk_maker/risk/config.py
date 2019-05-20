class FieldType:
    TEXT = 0
    NUMBER = 1
    DATE = 2
    CHOICE = 3

    CHOICES = (
        (TEXT, "Text"),
        (NUMBER, "Number"),
        (DATE, "Date"),
        (CHOICE, "Choice"),
    )
