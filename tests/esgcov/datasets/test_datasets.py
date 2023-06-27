from esgcov import HyFI


def test_datasets():
    HyFI.initialize()
    config = HyFI.compose("workflow=datasets")
    wf = HyFI.workflow_config(**config)
    HyFI.run_workflow(wf)


if __name__ == "__main__":
    test_datasets()
