"""This is module with fixtures for tests"""
from src.tick_tick import TickAPI
import pytest


@pytest.fixture(scope='module')
def authenticated_session():
    api = TickAPI('gipofe2520@asfalio.com', '123456789')
    return api


@pytest.fixture(scope='module')
def test_project_names():
    return ['TestProject1', 'TestProject2', 'TestProject3']


@pytest.fixture(scope='module')
def test_task_titles():
    return ['TestTask1', 'TestTask2', 'TestTask3', 'TestTask4', 'TestTask5']


@pytest.fixture(scope='module')
def wrong_login_info():
    return ['TestLogin', 'TestPassword']


@pytest.fixture(scope='module')
def successful_login_info():
    return ['gipofe2520@asfalio.com', '123456789']


@pytest.fixture(scope='module')
def test_projects(authenticated_session: TickAPI, test_project_names, test_project_colours):
    projects_id = authenticated_session.get_projects_id()
    for i in projects_id:
        authenticated_session.delete_project(authenticated_session.get_project_by_id(i)['name'])

    project1 = authenticated_session.add_project(test_project_names[0], test_project_colours[0])
    project2 = authenticated_session.add_project(test_project_names[1], test_project_colours[1])
    project3 = authenticated_session.add_project(test_project_names[2], test_project_colours[2])
    return [project1, project2, project3]


@pytest.fixture(scope='module')
def test_tasks(authenticated_session: TickAPI, test_task_titles, test_project_names, test_projects):
    projects_id = authenticated_session.get_projects_id()
    task1 = authenticated_session.add_task(test_task_titles[0], projects_id[0], 'TestContent1')
    task2 = authenticated_session.add_task(test_task_titles[1], projects_id[1], 'TestContent2')
    task3 = authenticated_session.add_task(test_task_titles[2], projects_id[2], 'TestContent3')
    task4 = authenticated_session.add_task(test_task_titles[3], projects_id[0], 'TestContent4')
    task5 = authenticated_session.add_task(test_task_titles[4], projects_id[1], 'TestContent5')
    return [task1, task2, task3, task4, task5]


@pytest.fixture(scope='module')
def tags_names():
    return ['mytesttag', 'anothertesttag', 'mycooltag']


@pytest.fixture(scope='module')
def tags_colours():
    return ['red', 'blue', 'green']


@pytest.fixture(scope='module')
def test_tags(authenticated_session: TickAPI, tags_names, tags_colours):
    all_tags = authenticated_session.get_tags()
    for i in all_tags:
        authenticated_session.delete_tag(i['name'])
    tag1 = authenticated_session.add_tag(tags_names[0], tags_colours[0])
    tag2 = authenticated_session.add_tag(tags_names[1], tags_colours[1])
    tag3 = authenticated_session.add_tag(tags_names[2], tags_colours[2])
    return [tag1, tag2, tag3]


@pytest.fixture(scope='module')
def test_project_colours():
    return ['red', 'purple', 'turquoise']
