import copy
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

    def calculate_seidel(self):
        x = [[0 for j in range(len(self.vector_b))] for i in range(1)]
        i = 0
        while True:
            x.append(self.seidel(x[i]))
            i += 1
            if len(x) >= 2 and max([fabs(x[i][j] - x[i - 1][j]) for j in range(len(x[0]))]) < self.e:
                self.result = x[i]
                return x[i]

    def seidel(self, x):
        n = len(self.matrix_a)
        cur_x = copy.deepcopy(x)
        for j in range(0, n):
            d = copy.deepcopy(self.vector_b[j])
            for i in range(0, n):
                if j != i:
                    d -= self.matrix_a[j][i] * cur_x[i]
            cur_x[j] = d / self.matrix_a[j][j]
        return cur_x
