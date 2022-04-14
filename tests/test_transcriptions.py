# TODO: the connector is ready for the tests, I just haven't written them yet.

from escriptorium_connector.dtos import PostTranscription, CharacterGraph
from .helpers import PrepForTranscriptionTest


def test_transcriptions():
    with PrepForTranscriptionTest() as (
        escr,
        new_document,
        new_part,
        new_line,
        new_trans_layer,
    ):
        content = "test"
        graphs = [
            CharacterGraph(
                c="t", poly=[[3, 3], [3, 6], [6, 6], [6, 3], [3, 3]], confidence=1.0
            ),
            CharacterGraph(
                c="e", poly=[[3, 3], [3, 6], [6, 6], [6, 3], [3, 3]], confidence=1.0
            ),
            CharacterGraph(
                c="s", poly=[[3, 3], [3, 6], [6, 6], [6, 3], [3, 3]], confidence=1.0
            ),
            CharacterGraph(
                c="t", poly=[[3, 3], [3, 6], [6, 6], [6, 3], [3, 3]], confidence=1.0
            ),
        ]
        new_transcription_data = PostTranscription(
            line=new_line.pk,
            transcription=new_trans_layer.pk,
            content=content,
            graphs=graphs,
        )
        new_transcription = escr.create_document_part_transcription(
            new_document.pk, new_part.pk, new_transcription_data
        )

        assert new_transcription.content == content
        assert new_transcription.line == new_line.pk
        assert new_transcription.pk != 0
        assert len(new_transcription.graphs) == len(graphs)
        for g1, g2 in zip(new_transcription.graphs, graphs):
            assert g1.c == g2.c
            assert g1.confidence == g2.confidence
            for point1, point2 in zip(g1.poly, g2.poly):
                assert point1[0] == point2[0]
                assert point1[1] == point2[1]
