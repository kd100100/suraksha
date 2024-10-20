from abc import ABC, abstractmethod


class Validator(ABC):
    @abstractmethod
    def validate(self, data: str) -> dict:
        """
        Validate the input data and return a dictionary with the validation results.

        :param data: The input data to validate
        :return: A dictionary containing the validation results
        """
        pass
