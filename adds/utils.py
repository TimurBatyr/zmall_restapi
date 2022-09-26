from adds.models import ReviewPost


def multiple_images(post, image):
    dict = {}
    dict['post'] = post
    dict['image'] = image
    return dict


def sql_recursive():
    sql_tree = '''with recursive tree (id, text, email, post_id, parent_id)
            as (select id, text, email, post_id, parent_id  from adds_reviewpost where parent_id is null
        union all
           select adds_reviewpost.id, adds_reviewpost.text, adds_reviewpost.email,
           adds_reviewpost.post_id, adds_reviewpost.parent_id from adds_reviewpost
             inner join tree on tree.id = adds_reviewpost.parent_id)
        select id, text, email, post_id, parent_id from tree
    '''

    return ReviewPost.objects.raw(sql_tree)

