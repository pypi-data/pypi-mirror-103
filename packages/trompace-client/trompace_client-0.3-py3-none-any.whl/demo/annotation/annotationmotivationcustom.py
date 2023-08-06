# Perform annotations using a custom set of motivations defined by a custom object
from demo import send_query_and_get_id
from demo.annotation import audio_file_liebestraum
from demo.definedterm import motivation_collection
from trompace.mutations import annotation


def main(print_queries: bool, submit_queries: bool):
    user_vcard = "https://testuser.trompa-solid.upf.edu/profile/card#me"

    audio_id = audio_file_liebestraum(print_queries, submit_queries)

    # Linking Annotation, this joins together the two previous annotations into a third one
    # Make a custom motivation which describes what this linking represents
    custom_motivation = annotation.create_annotation_motivation(
        creator=user_vcard, title="Music scholars feedback grouping",
        description="This motivation groups together 4 different annotations into a single meta-annotation"
                    "which represents the full description of a recording by a user",
        broader_schema=annotation.AnnotationSchemaMotivation.linking)
    custom_motivation_id = "custom-motivation-id"
    print("Linking Annotation - create Motivation")
    if print_queries:
        print(custom_motivation)
    if submit_queries:
        custom_motivation_id = send_query_and_get_id(custom_motivation, "CreateAnnotationCEMotivation")

    # The annotation target. We're annotating the URL that is at the `source` field of the above audio object
    target = annotation.create_annotation_ce_target(
        creator=user_vcard,
        field="source",  # we want to annotate the URL that is at the 'source' field of the AudioObject node
    )

    target_id = "ce-target-id"
    print("AnnotationCETarget")
    if print_queries:
        print(target)
    if submit_queries:
        target_id = send_query_and_get_id(target, "CreateAnnotationCETarget")

    print("Join AnnotationCETarget-Target")
    target_join = annotation.merge_annotation_target_target(target_id, audio_id)
    if print_queries:
        print(target_join)
    if submit_queries:
        send_query_and_get_id(target_join)

    # The annotation
    ann = annotation.create_annotation(
        creator=user_vcard,
        motivation=annotation.AnnotationSchemaMotivation.commenting,
        # A specific motivation which is skos:Broader of oa:commenting, specifically for giving praise
        motivation_url="https://example.com/schema/motivations#praise"
    )

    ann_id = "annotation-id"
    print("Annotation")
    if print_queries:
        print(ann)
    if submit_queries:
        ann_id = send_query_and_get_id(ann, "CreateAnnotation")

    # Join the annotation with the AnnotationCETarget
    annotation_target_join = annotation.merge_annotation_targetnode(ann_id, target_id)

    print("Annotation - link to target")
    if print_queries:
        print(annotation_target_join)
    if submit_queries:
        send_query_and_get_id(annotation_target_join)


if __name__ == '__main__':
    from demo import args, send_query_and_get_id

    main(args.args.print, args.args.submit)


link_annotation_motivation_join = annotation.merge_annotation_cemotivation(ann_link_id, custom_motivation_id)
