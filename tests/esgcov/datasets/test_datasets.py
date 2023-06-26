from esgcov import HyFI


def test_datasets():
    HyFI.initialize()
    config = HyFI.compose("task=datasets", overrides=["+project=esgcov"])
    task = HyFI.task_config(**config)
    HyFI.run_task_pipelines(task)


if __name__ == "__main__":
    test_datasets()
