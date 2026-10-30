# Rollback and release hold

No production state changed in this task. Main baseline is b553356528d097632f4f30da40258af4501f8212. Design baseline is 86fa3c68c65c0fc722b1a176c9f64e094e04d782.

Before release: review the candidate commit, public URL, 404 behavior, contact mock test results, all third-party entry points and language coverage. Obtain explicit approval. Merge/deploy remains a separate action.

To undo the isolated upgrade, create a normal revert commit of this task's candidate commit on the design branch. Do not force-push or reset main. Old files were retained. To undo a later authorized production release, restore its prior deployed version through the same Worker and verify the original URL map and contact path. No DNS or payment changes are needed.
