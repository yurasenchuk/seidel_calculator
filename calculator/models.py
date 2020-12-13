import copy
import time
from concurrent.futures._base import LOGGER
from math import fabs

from django.contrib.postgres.fields import ArrayField
from django.db import models, IntegrityError, DataError
from user.models import CustomUser


class Calculator(models.Model):
    size = models.IntegerField(default=0)
    matrix_a = ArrayField(ArrayField(models.CharField(max_length=10, blank=True), size=0), size=0, blank=True)
    vector_b = ArrayField(models.CharField(max_length=10, blank=True), size=0, blank=True)
    result = ArrayField(models.CharField(max_length=10, blank=True), size=0, blank=True)
    e = models.FloatField(default=0.001)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    @staticmethod
    def create(size, matrix_a, vector_b, e, user):
        calculator = Calculator(size=size, matrix_a=matrix_a, vector_b=vector_b, e=e, user=user,
                                result=[0 for i in range(size)])
        try:
            calculator.save()
            return calculator
        except (IntegrityError, AttributeError, DataError, ValueError) as err:
            LOGGER.error("Wrong attributes or relational integrity error")

    def update(self, result):
        self.result = result
        self.save()

    @staticmethod
    def get_by_id(calculator_id):
        try:
            calculator = Calculator.objects.get(id=calculator_id)
            return calculator
        except CustomUser.DoesNotExist:
            LOGGER.error("User does not exist")
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "matrix_a": self.matrix_a,
            "vector_b": self.vector_b,
            "result": self.result,
            "e": self.e}

    def calculate_seidel(self):
        start = float(time.time()/1000)
        x = [[0 for j in range(len(self.vector_b))] for i in range(1)]
        matrix = [[float(self.matrix_a[i][j]) for j in range(self.size)] for i in range(self.size)]
        vector = [float(self.vector_b[j]) for j in range(self.size)]
        i = 0
        while True:
            step = float(time.time() / 1000)
            if step - start >= 200:
                return False
            x.append(self.seidel(x[i], matrix, vector))
            i += 1
            if len(x) >= 2 and max([fabs(x[i][j] - x[i - 1][j]) for j in range(len(x[0]))]) < self.e:
                return x[i]

    def seidel(self, x, matrix, vector):
        n = len(matrix)
        cur_x = copy.deepcopy(x)
        for j in range(0, n):
            d = copy.deepcopy(vector[j])
            for i in range(0, n):
                if j != i:
                    d -= matrix[j][i] * cur_x[i]
            cur_x[j] = d / matrix[j][j]
        return cur_x

    @staticmethod
    def results(user_id):
        return list(Calculator.objects.all().filter(user_id=user_id))

    @staticmethod
    def delete_by_user_id(user_id):
        try:
            tasks = Calculator.results(user_id)
            for i in tasks:
                i.delete()
            return True
        except Calculator.DoesNotExist:
            LOGGER.error("Task does not exist")
        return False
