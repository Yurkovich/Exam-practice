const API_BASE_URL = 'http://127.0.0.1:8000/api/task';
const taskFields = ['edit-name', 'edit-description', 'edit-datetime'];

taskFields.forEach(fieldId => {
    const field = document.getElementById(fieldId);
    field.addEventListener('input', handleTaskEdit);
});

async function handleTaskEdit() {
    const idField = document.getElementById('edit-id');
    const id = idField.value.trim();

    if (!id) return;

    const taskElement = document.querySelector(`.task-list__item[data-id="${id}"]`);
    if (taskElement && taskElement.classList.contains('completed')) {
        taskElement.classList.remove('completed');
        await updateTaskStatus(id, 0);
    }
}

async function updateTaskStatus(taskId, status) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/task/${taskId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ completed: status }),
        });

        if (!response.ok) {
            console.error('Не удалось обновить статус задачи');
        }
    } catch (error) {
        console.error('Ошибка при обновлении статуса задачи:', error.message);
    }
}

async function createTask() {
    const name = document.getElementById('add-name').value;
    const description = document.getElementById('add-description').value;
    const datetime = document.getElementById('add-datetime').value;

    const taskData = {
        name,
        description,
        datetime,
        completed: 0
    };

    try {
        const response = await fetch(API_BASE_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(taskData)
        });

        if (response.ok) {
            const result = await response.json();
            alert('Задача успешно создана!');
            console.log(result);
            addTaskToList(result);
            await updateTaskList();
        } else {
            const errorText = await response.text();
            alert('Ошибка при создании задачи: ' + errorText);
            console.error(errorText);
        }
    } catch (error) {
        alert('Ошибка при выполнении запроса: ' + error.message);
        console.error(error);
    }
}

async function loadTaskData() {
    const idField = document.getElementById('edit-id');
    const nameField = document.getElementById('edit-name');
    const descriptionField = document.getElementById('edit-description');
    const datetimeField = document.getElementById('edit-datetime');

    const id = idField.value.trim();

    if (!id) {
        nameField.value = '';
        descriptionField.value = '';
        datetimeField.value = '';
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/task/${id}`, {
            method: 'GET',
        });

        if (response.ok) {
            const task = await response.json();
            nameField.value = task.name || '';
            descriptionField.value = task.description || '';
            datetimeField.value = task.datetime.replace(' ', 'T') || '';
        } else {
            idField.value = '';
            nameField.value = '';
            descriptionField.value = '';
            datetimeField.value = '';
        }
    } catch (error) {
        console.error('Ошибка при выполнении запроса:', error.message);
        idField.value = '';
        nameField.value = '';
        descriptionField.value = '';
        datetimeField.value = '';
    }
}

async function updateTask() {
    const id = document.getElementById('edit-id').value;
    if (!id) {
        alert('Не указан ID задачи для обновления.');
        return;
    }

    const name = document.getElementById('edit-name').value;
    const description = document.getElementById('edit-description').value;
    const datetime = document.getElementById('edit-datetime').value;

    const taskData = { id, name, description, datetime, completed: 0 };

    try {
        const response = await fetch(`${API_BASE_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(taskData)
        });

        if (response.ok) {
            const result = await response.json();
            alert('Задача успешно обновлена!');
            console.log(result);
            await updateTaskList();
        } else {
            const errorText = await response.text();
            alert('Ошибка при обновлении задачи: ' + errorText);
            console.error(errorText);
        }
    } catch (error) {
        alert('Ошибка при выполнении запроса: ' + error.message);
        console.error(error);
    }
}

async function markTaskAsCompleted() {
    const id = document.getElementById('edit-id').value;

    if (!id) {
        alert('Введите ID задачи!');
        return;
    }

    const taskData = { completed: 1 };

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/task/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        });

        if (response.ok) {
            const result = await response.json();
            alert('Задача успешно выполнена!');
            console.log(result);

            const taskItems = document.querySelectorAll('.task-list__item');
            taskItems.forEach((taskItem) => {
                const taskName = taskItem.querySelector('.task-list__item-name');
                if (taskName && taskName.textContent === result.name) {
                    taskItem.classList.add('completed');
                }
            });

            await updateTaskList();
        } else {
            const errorText = await response.text();
            alert('Ошибка при обновлении задачи: ' + errorText);
            console.error(errorText);
        }
    } catch (error) {
        alert('Ошибка при выполнении запроса: ' + error.message);
        console.error(error);
    }
}

function addTaskToList(task) {
    const taskList = document.getElementById('task-list');

    const taskItem = document.createElement('div');
    taskItem.className = 'task-list__item';
    taskItem.dataset.taskId = task.id;

    if (task.completed) {
        taskItem.classList.add('completed');
    }

    const taskHeader = document.createElement('div');
    taskHeader.className = 'task-list__header';

    const taskName = document.createElement('h3');
    taskName.className = 'task-list__item-name';
    taskName.textContent = `[ ${task.id} ] ${task.name}`;

    const deleteButton = document.createElement('button');
    deleteButton.className = 'task-item__delete';
    deleteButton.textContent = '×';
    deleteButton.setAttribute('aria-label', 'Удалить задачу');

    deleteButton.addEventListener('click', async () => {
        await deleteTask(task.id, taskItem);
    });

    taskHeader.appendChild(taskName);
    taskHeader.appendChild(deleteButton);

    const taskDesc = document.createElement('p');
    taskDesc.className = 'task-list__item_desc';
    taskDesc.textContent = task.description;

    const taskDeadline = document.createElement('div');
    taskDeadline.className = 'task-list__item-deadline';
    const deadlineText = document.createElement('p');
    deadlineText.textContent = `Дедлайн: ${new Date(task.datetime).toLocaleString()}`;
    taskDeadline.appendChild(deadlineText);

    taskItem.appendChild(taskHeader);
    taskItem.appendChild(taskDesc);
    taskItem.appendChild(document.createElement('br'));
    taskItem.appendChild(taskDeadline);

    taskList.appendChild(taskItem);
}

async function deleteTask(taskId, taskElement) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/task/${taskId}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            const result = await response.json();
            alert(result.message);
            taskElement.remove();
        } else {
            const errorText = await response.text();
            alert('Ошибка при удалении задачи: ' + errorText);
            console.error(errorText);
        }
    } catch (error) {
        alert('Ошибка при выполнении запроса: ' + error.message);
        console.error(error);
    }
}

async function updateTaskList() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/task', {
            method: 'GET'
        });

        if (response.ok) {
            const tasks = await response.json();
            const taskList = document.getElementById('task-list');
            taskList.innerHTML = '';

            tasks.forEach(task => {
                addTaskToList(task);
            });
        } else {
            const errorText = await response.text();
            alert('Ошибка при получении списка задач: ' + errorText);
            console.error(errorText);
        }
    } catch (error) {
        alert('Ошибка при выполнении запроса: ' + error.message);
        console.error(error);
    }
}
window.onload = updateTaskList;