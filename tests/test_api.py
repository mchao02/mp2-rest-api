def test_upload_csv(client, sample_csv_bytes):
    response = client.post(
        "/upload",
        files={
            "file": ("sample_data.csv", sample_csv_bytes, "text/csv")
        }
    )

    assert response.status_code == 200

    result = response.json()
    assert result["rows"] == 6
    assert result["columns"] == 2
    assert isinstance(result["id"], int)
    assert result["id"] > 0


def test_process_and_retrieve(
    client, uploaded_dataset_id, processing_body
):
    response = client.post(
        f"/datasets/{uploaded_dataset_id}/process",
        json=processing_body
    )

    assert response.status_code == 200

    result = response.json()
    assert result["validation_rows_removed"] == 1
    assert result["cleaning_report"]["rows_before"] == 5
    assert result["cleaning_report"]["rows_after"] == 3
    assert result["cleaning_report"]["rows_removed"] == 2

    response = client.get(f"/datasets/{uploaded_dataset_id}")

    assert response.status_code == 200

    result = response.json()
    assert result["total_rows"] == 3
    assert result["data"] == [
        {"student_id": 1, "score": 80},
        {"student_id": 2, "score": 90},
        {"student_id": 5, "score": 85}
    ]


def test_retrieve_missing_dataset(client):
    response = client.get("/datasets/999")

    assert response.status_code == 404