from adds.models import ReviewPost


def multiple_images(post, image):
    dict = {}
    dict['post'] = post
    dict['image'] = image
    return dict


def sql_recursive():
    sql_tree = '''with recursive (id, text, email_id, post_id, parent_id)
            as (select id, text, email_id, post_id, parent_id  from advert_comment where parent_id is null
        union all
           select advert_comment.id, advert_comment.text, advert_comment.advert_id,
                  advert_comment.parent_id, advert_comment.user_id from advert_comment
             inner join tree on tree.id = advert_comment.parent_id)
        select id, text, advert_id, parent_id, user_id from tree
    '''

    return ReviewPost.objects.raw(sql_tree)

