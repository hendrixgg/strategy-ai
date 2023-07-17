from task import BaseTask


class T1Surfacing(BaseTask):
    def __init__(self):
        super().__init__(1, "t1_surfacing")

    def generate_results(self):
        for step in super().generate_results():
            yield step
        yield "task 1 surfacing generator"


if __name__ == "__main__":
    testTask1 = T1Surfacing()
    for step in testTask1.generate_results():
        print(step)

    print("the task id is:", testTask1.unique_id)
