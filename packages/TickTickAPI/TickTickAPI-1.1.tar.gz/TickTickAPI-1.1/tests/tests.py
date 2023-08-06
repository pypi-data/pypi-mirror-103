from src.tick_tick import TickAPI
import pytest


# ToDO:
#       1. Сделать пакет из проекта (туториал на офф сайте)


def test_successful_tick_authorization(successful_login_info):
    TickAPI(successful_login_info[0], successful_login_info[1])


def test_fail_tick_authorization(wrong_login_info):
    with pytest.raises(AttributeError):
        TickAPI(wrong_login_info[0], wrong_login_info[1])


def test_successful_get_project_by_name(authenticated_session: TickAPI, test_projects, test_project_names):
    project = authenticated_session.get_project_by_name(test_project_names[0])
    assert project['name'] == test_projects[0]


def test_get_not_existing_project_by_name(authenticated_session: TickAPI):
    project = authenticated_session.get_project_by_name('someawfulname')
    assert project == {}


def get_tasks_by_project_id(authenticated_session: TickAPI, test_tasks):
    projects_id = authenticated_session.get_projects_id()
    tasks1 = authenticated_session.get_tasks_by_project_id(projects_id[0])
    assert tasks1[0]['title'] == test_tasks[3]
    assert tasks1[1]['title'] == test_tasks[0]
    tasks2 = authenticated_session.get_tasks_by_project_id(projects_id[1])
    assert tasks2[0]['title'] == test_tasks[4]
    assert tasks2[1]['title'] == test_tasks[1]
    tasks3 = authenticated_session.get_tasks_by_project_id(projects_id[2])
    assert tasks3[0]['title'] == test_tasks[2]


def test_get_projects_id(authenticated_session: TickAPI, test_projects):
    projects_id = authenticated_session.get_projects_id()
    assert projects_id[0] == authenticated_session.get_project_by_name(test_projects[0])['id']
    assert projects_id[1] == authenticated_session.get_project_by_name(test_projects[1])['id']
    assert projects_id[2] == authenticated_session.get_project_by_name(test_projects[2])['id']


def test_get_tags(authenticated_session: TickAPI, test_tags):
    my_tags = authenticated_session.get_tags()
    assert my_tags[0]['name'] == test_tags[1]
    assert my_tags[1]['name'] == test_tags[2]
    assert my_tags[2]['name'] == test_tags[0]


def test_get_tag_by_name(authenticated_session: TickAPI, test_tags):
    my_tag1 = authenticated_session.get_tag_by_name(test_tags[0])
    my_tag2 = authenticated_session.get_tag_by_name(test_tags[1])
    my_tag3 = authenticated_session.get_tag_by_name(test_tags[2])
    assert my_tag1['name'] == test_tags[0]
    assert my_tag2['name'] == test_tags[1]
    assert my_tag3['name'] == test_tags[2]


def test_get_tasks_by_title(authenticated_session: TickAPI, test_tasks):
    task1 = authenticated_session.get_tasks_by_title(test_tasks[0])
    assert task1[0]['title'] == test_tasks[0]
    task2 = authenticated_session.get_tasks_by_title(test_tasks[1])
    assert task2[0]['title'] == test_tasks[1]
    task3 = authenticated_session.get_tasks_by_title(test_tasks[2])
    assert task3[0]['title'] == test_tasks[2]
    task4 = authenticated_session.get_tasks_by_title(test_tasks[3])
    assert task4[0]['title'] == test_tasks[3]


def test_add_task(authenticated_session: TickAPI):
    projects_id = authenticated_session.get_projects_id()
    task1 = authenticated_session.add_task('OnlyOneTask', projects_id[0], 'TestContent1')
    task2 = authenticated_session.add_task('SecondAwesomeTask', projects_id[1], 'TestContent2')
    assert task1 == "OnlyOneTask"
    assert task2 == 'SecondAwesomeTask'


def test_add_task_with_tag(authenticated_session: TickAPI, test_tags, test_projects):
    projects_id = authenticated_session.get_projects_id()
    my_task = authenticated_session.add_task('UniqueTask',
                                             projects_id[1],
                                             'awesomecontent',
                                             [test_tags[0]]
                                             )
    assert my_task == 'UniqueTask'


def test_add_task_failed_duplicate_title(authenticated_session: TickAPI, test_projects):
    projects_id = authenticated_session.get_projects_id()
    authenticated_session.add_task('DuplicateName',
                                   projects_id[1],
                                   'awesomecontent',
                                   )
    with pytest.raises(Exception):
        authenticated_session.add_task('DuplicateName',
                                       projects_id[1],
                                       'awesomecontent',
                                       )


def test_get_projects_by_colour(authenticated_session: TickAPI, test_projects, test_project_colours):
    red_project = authenticated_session.get_projects_by_colour(test_project_colours[0])
    assert red_project[0]['name'] == test_projects[0]
    purple_project = authenticated_session.get_projects_by_colour(test_project_colours[1])
    assert purple_project[0]['name'] == test_projects[1]
    turquoise_project = authenticated_session.get_projects_by_colour(test_project_colours[2])
    assert turquoise_project[0]['name'] == test_projects[2]


def test_get_projects_with_wrong_colour(authenticated_session: TickAPI):
    with pytest.raises(KeyError):
        authenticated_session.get_projects_by_colour('BadColour')


def test_get_zero_projects_by_colour(authenticated_session: TickAPI, test_projects):
    green_projects = authenticated_session.get_projects_by_colour('green')
    assert [] == green_projects


def test_add_tag(authenticated_session: TickAPI, tags_colours):
    tag1 = authenticated_session.add_tag('unrealtag', tags_colours[0])
    assert tag1 == 'unrealtag'


def test_add_tag_with_duplicate_name(authenticated_session: TickAPI):
    authenticated_session.add_tag('duplicatetag')
    with pytest.raises(Exception):
        authenticated_session.add_tag('duplicatetag')


def test_add_tag_with_wrong_colour(authenticated_session: TickAPI):
    with pytest.raises(KeyError):
        authenticated_session.add_tag('cooltag', 'badcolour')


def test_add_project_with_wrong_colour(authenticated_session: TickAPI):
    with pytest.raises(KeyError):
        authenticated_session.add_project('MyCoolProject', 'wrong_colour')


def test_add_project__failed_duplicate_name(authenticated_session: TickAPI):
    with pytest.raises(Exception):
        authenticated_session.add_project('CommonProject', 'blue')
        authenticated_session.add_project('CommonProject', 'red')


def test_successful_add_project(authenticated_session: TickAPI):
    project = authenticated_session.add_project('AwesomeProject', 'red')
    assert project == 'AwesomeProject'


def test_get_project_by_id(authenticated_session: TickAPI, test_projects):
    projects_id = authenticated_session.get_projects_id()
    awesome_project = authenticated_session.get_project_by_id(projects_id[0])
    assert awesome_project['name'] == test_projects[0]


def test_delete_tag(authenticated_session: TickAPI):
    tag = authenticated_session.add_tag('mygreattag', 'blue')
    deleted_tag = authenticated_session.delete_tag(tag)
    assert deleted_tag == tag


def test_delete_not_existing_tag(authenticated_session: TickAPI):
    with pytest.raises(Exception):
        authenticated_session.delete_tag('NotExistingTag')


def test_delete_project(authenticated_session: TickAPI):
    project = authenticated_session.add_project('UniqueProject', 'blue', 'TASK')
    project_id = authenticated_session.get_project_by_name(project)['id']
    deleted_project_id = authenticated_session.delete_project('UniqueProject')
    assert project_id == deleted_project_id


def test_delete_not_existing_project(authenticated_session: TickAPI):
    with pytest.raises(Exception):
        authenticated_session.delete_project('NotExistingProject')


def test_delete_task(authenticated_session: TickAPI):
    projects = authenticated_session.get_projects_id()
    tags = authenticated_session.get_tags()
    authenticated_session.add_task('TESTTASK', projects[0], 'content', [tags[0]['name']])
    task_id = authenticated_session.get_tasks_by_title('TESTTASK')
    deleted_task = authenticated_session.delete_task('TESTTASK', projects[0])
    assert deleted_task == task_id[0]['id']


def test_delete_not_existing_task(authenticated_session: TickAPI):
    with pytest.raises(Exception):
        authenticated_session.delete_task('NotExistingTask', '123456789')


def test_empty_trash(authenticated_session: TickAPI):
    success = authenticated_session.empty_trash()
    assert success == 0
