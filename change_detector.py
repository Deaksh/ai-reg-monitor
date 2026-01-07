def detect_changes(old_chunks, new_chunks):
    changes = []

    old_map = {c["chunk_id"]: c for c in old_chunks}
    new_map = {c["chunk_id"]: c for c in new_chunks}

    # Modified or removed
    for chunk_id, old_chunk in old_map.items():
        new_chunk = new_map.get(chunk_id)

        if not new_chunk:
            changes.append({
                "chunk_id": chunk_id,
                "before": old_chunk["text"],
                "after": "",
                "change_kind": "REMOVED"
            })
            continue

        if old_chunk["hash"] != new_chunk["hash"]:
            changes.append({
                "chunk_id": chunk_id,
                "before": old_chunk["text"],
                "after": new_chunk["text"],
                "change_kind": "MODIFIED"
            })

    # Newly added
    for chunk_id, new_chunk in new_map.items():
        if chunk_id not in old_map:
            changes.append({
                "chunk_id": chunk_id,
                "before": "",
                "after": new_chunk["text"],
                "change_kind": "ADDED"
            })

    return changes
