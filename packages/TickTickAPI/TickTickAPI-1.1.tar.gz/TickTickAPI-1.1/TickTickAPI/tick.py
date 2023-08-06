"""This module contains functional code of TickTickAPI"""
from typing import List
import requests


class TickAPI:

    def __init__(self, username: str, passwd: str):
        """Initialize user`s session.
           Args:
               username (str): login.
               passwd (str): passwd.
           Returns:
        """
        self.base_url = 'https://api.ticktick.com/api/v2'
        self.colours = {
            "purple": "#DA70D6",
            'blue': '#000080',
            'green': '#008000',
            'red': '#EC6666',
            'yellow': '#FFFF00',
            'turquoise': '#00FFFF',
            'light blue': '#4AA6EF',
        }
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json',
            'accept': '*/*',
            'user-agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                ' (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        }
        request = self.session.post(f"{self.base_url}/user/signon?wc=true", json={
            'username': f'{username}',
            'password': f'{passwd}',
        })
        if request.status_code == 200:
            token = request.json()['token']
            client_id = request.json()['userId']
            self.token = token
            self.client_id = client_id
        else:
            raise AttributeError('Wrong login or password')

    def get_projects_id(self) -> List[str]:
        """Gets all IDs of existing projects.
           Args:
           Returns:
            List[str]: IDs of existing projects.
        """
        projects = list()
        url = f'{self.base_url}/projects'
        request = self.session.get(url)
        if request.status_code == 200:
            data = request.json()
            for i in data:
                id_ = i['id']
                projects.append(id_)
        else:
            raise Exception(f'Failed to get projects, error code is {request.status_code}')
        return projects

    def get_tasks_by_project_id(self, project_id: str) -> list:
        """Gets all tasks in the project.
           Args:
               project_id (str): Project ID.
           Returns:
               list: All tasks in the project.
       """
        tasks_list = list()
        url = f'{self.base_url}/batch/check/1'
        request = self.session.get(url)
        if request.status_code != 200:
            raise Exception('Failed to get project tasks')
        data = request.json()
        tasks = data['syncTaskBean']['update']
        for task in tasks:
            if task['projectId'] == project_id:
                tasks_list.append(task)
        return tasks_list

    def get_completed_tasks_by_project_id(self, project_id: str, count: int) -> List[dict]:
        """Gets completed tasks in the project.
            Args:
                project_id (str): Project ID.
                count (int): The number of tasks to get.
            Returns:
                List[dict]: Completed tasks in the project.
        """
        url = f'{self.base_url}/project/{project_id}/completed/?limit={count}'
        request = self.session.get(url)
        if request.status_code != 200:
            raise Exception(f'Failed to get completed tasks, error code is {request.status_code}')
        return request.json()

    def get_tags(self) -> List[dict]:
        """Gets all existing tags.
            Args:
            Returns:
                List[dict]: All tags.
        """
        url = f'{self.base_url}/batch/check/1'
        request = self.session.get(url)
        if request.status_code != 200:
            raise Exception(f'Failed to get tags, error code is {request.status_code}')
        tags = request.json()['tags']
        return tags

    def get_tag_by_name(self, name: str) -> dict:
        """Get a tag by name.
            Args:
                name (str): Tag name.
            Returns:
                dict: Found tag.
        """
        tags = self.get_tags()
        for tag in tags:
            if tag['name'] == name:
                return tag
        return {}

    def get_tasks_by_title(self, title: str, project_id: str = None) -> List[dict]:
        """Get tasks by name.
            Args:
                title (str): The name of the project.
                project_id (str): ID of the project in which we are looking for tasks.
            Returns:
               List[dict]: One task if the project is set otherwise
                 all found tasks in all projects.
        """
        tasks_by_title = list()
        if project_id:
            tasks = self.get_tasks_by_project_id(project_id)
            for task in tasks:
                if task['title'] == title:
                    tasks_by_title.append(task)
            return tasks_by_title
        projects = self.get_projects_id()
        for _id in projects:
            tasks = self.get_tasks_by_project_id(_id)
            for task in tasks:
                if task['title'] == title:
                    tasks_by_title.append(task)
        return tasks_by_title

    def get_project_by_id(self, project_id: str) -> dict:
        """Get a project by ID.
            Args:
                project_id (str): Project ID.
            Returns:
                dict: Project.
        """
        url = f'{self.base_url}/projects'
        request = self.session.get(url)
        if request.status_code != 200:
            raise Exception(f'Failed to get the task list, error code is {request.status_code}')
        projects = request.json()
        for project in projects:
            if project['id'] == project_id:
                return project
        return {}

    def get_project_by_name(self, name: str) -> dict:
        """Get a project by name.
            Args:
                name (str): The name of the project.
            Returns:
                dict: Project.
        """
        url = f'{self.base_url}/projects'
        request = self.session.get(url)
        if request.status_code != 200:
            raise Exception(f'Failed to get the task list, error code is {request.status_code}')
        projects = request.json()
        for project in projects:
            if project['name'] == name:
                return project
        return {}

    def get_projects_by_colour(self, colour: str) -> List[dict]:
        """Get a project by color.
            Args:
                colour (str): Project color.
            Returns:
               List[dict]: All projects of a given color.
        """
        if colour.lower() not in self.colours.keys():
            raise KeyError(f'So far, {colour} colour is not supported.')
        projects_by_colour = list()
        url = f'{self.base_url}/projects'
        request = self.session.get(url)
        if request.status_code != 200:
            raise Exception(f'Failed to get the task list, error code is {request.status_code}')
        projects = request.json()
        for project in projects:
            if project['color'] == self.colours[colour.lower()]:
                projects_by_colour.append(project)
        return projects_by_colour

    def add_task(self, name: str, project_id: str, content: str = '', tag: list = None) -> str:
        """Add a task to a project.
            Args:
                name (str): Tag name.
                project_id (str): The ID of the project to which the task is added.
                content (str): Contents of the task.
                tag (dict): Task tag.
            Returns:
                str: The name of the created task.
        """
        if self.get_tasks_by_title(name, project_id):
            raise Exception('A task with the same name already exists!')
        if tag is None:
            tag = []
        url = f'{self.base_url}/batch/task'
        data = {"add": [
            {"items": [], "reminders": [], "exDate": [],
             "dueDate": 'null', "priority": 0, "progress": 0, "assignee": 'null',
             "sortOrder": -1099511627776, "startDate": 'null', "isFloating": 'false',
             "status": 0, "projectId": f"{project_id}", "kind": 'null', "createdTime": "",
             "modifiedTime": "", "title": f"{name}", "tags": tag, "timeZone": "Europe/Moscow",
             "content": f"{content}", "id": ""}], "update": [], "delete": []}
        request = self.session.post(url, json=data)
        if request.status_code != 200:
            raise Exception(f'Failed to create task, error code is {request.status_code}')
        return name

    def add_tag(self, tag_name: str, colour: str = None, parent: str = None) -> str:
        """Add a tag with a name and color.
            Args:
                tag_name (str): The name of the project.
                colour (str): Tag color.
                parent (dict): The parent tag.
            Returns:
                 str: The name of the created tag.
            """
        if self.get_tag_by_name(tag_name):
            raise Exception('This tag already exists!')
        if colour and colour.lower() not in self.colours.keys():
            raise KeyError(f'So far, {colour} colour is not supported..')
        url = f'{self.base_url}/batch/tag'
        data = {"add": [
            {"color": self.colours[colour.lower()] if colour else None,
             "parent": f'{parent}',
             "name": f"{tag_name}",
             "sortOrder": -2199023255552, "label": f"{tag_name}",
             "sortType": "project"}], "update": []
        }
        request = self.session.post(url, json=data)
        if request.status_code != 200:
            raise Exception(f'Failed to create tag, error code is {request.status_code}')
        return tag_name

    def add_project(self, project_title: str, colour: str = '',
                    type_of_project: str = 'TASK') -> str:
        """Add a project with a name and color.
            Args:
                project_title (str): The name of the project.
                colour (str): Project color.
                type_of_project (str): Project type.
            Returns:
                str: The name of the created project.
        """
        if self.get_project_by_name(project_title):
            raise Exception('This project already exists!')
        if colour and colour.lower() not in self.colours.keys():
            raise KeyError(f'So far, {colour} colour is not supported..')
        url = f'{self.base_url}/project'
        data = {
            "name": f"{project_title}",
            "color": f"{self.colours[colour.lower()] if colour else None}",
            "groupId": None,
            "sortOrder": -2199023255552,
            "inAll": True,
            "muted": False,
            "teamId": None,
            "kind": type_of_project,
            "isOwner": True
        }
        request = self.session.post(url, json=data)
        if request.status_code != 200:
            raise Exception(f'Failed to create project, error code is {request.status_code}')
        return project_title

    def delete_tag(self, name: str) -> str:
        """Remove a tag by name.
            Args:
                name (str): Tag name.
            Returns:
               str: The name of the removed tag.
        """
        tag = self.get_tag_by_name(name)
        if not tag:
            raise Exception('There is no such tag!')
        url = f'{self.base_url}/tag?name={name}'
        request = self.session.delete(url)
        if request.status_code != 200:
            raise ValueError(f'Unable to remove this tag, error code is {request.status_code}')
        return name

    def delete_project(self, name: str) -> str:
        """Remove a project by name.
            Args:
                    name (str): The name of the project.
            Returns:
                str: The ID of the removed project.
        """
        project = self.get_project_by_name(name)
        if not project:
            raise Exception('There is no such project!')
        project_id = project['id']
        url = f'{self.base_url}/batch/project'
        data = {"add": [], "update": [], "delete": [project_id]}
        request = self.session.post(url, json=data)
        if request.status_code != 200:
            raise Exception(f'Failed to delete project, error code is {request.status_code}')
        return project_id

    def delete_task(self, task_title: str, project_id: str) -> str:
        """Delete a task by name in a specific project.
            Args:
                task_title (str): Task name.
                project_id (str): The ID of the project in which we are deleting the task.
            Returns:
               str: The ID of the removed task.
        """
        task = self.get_tasks_by_title(task_title, project_id)
        if not task:
            raise Exception('There is no such task!')
        url = f'{self.base_url}/batch/task'
        data = {"delete": [
            {"taskId": f"{task[0]['id']}",
             "projectId": project_id
             }]
        }
        request = self.session.post(url, json=data)
        if request.status_code != 200:
            raise Exception(f'Failed to delete task, error code is {request.status_code}')
        return task[0]['id']

    def empty_trash(self):
        """Empty the bin.
            Args:
            Returns:
                int: 0
        """
        url = f'{self.base_url}/trash/empty'
        request = self.session.delete(url)
        if request.status_code != 200:
            raise Exception(f'Failed to empty trash, error code is {request.status_code}')
        return 0
