# Template Specifications

Detailed specifications for HTMX templates with exact implementations.

## Template Architecture

### Base Template (`templates/base.html`)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Todo App{% endblock %}</title>
    <script src="https://unpkg.com/htmx.org@1.9.6"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"></script>
    {% block extra_head %}{% endblock %}
</head>
<body class="bg-gray-100 min-h-screen">
    <nav class="bg-blue-600 text-white p-4">
        <h1 class="text-xl font-bold">Todo Application</h1>
    </nav>

    <main class="container mx-auto p-4">
        {% block content %}{% endblock %}
    </main>

    <div id="notification" class="fixed top-4 right-4 hidden"></div>
    {% block extra_body %}{% endblock %}
</body>
</html>
```

### Task List Template (`templates/tasks/list.html`)
```html
{% extends "base.html" %}

{% block title %}Tasks - Todo App{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto">
    <!-- Header with filters -->
    <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">My Tasks</h2>
        <button hx-get="/tasks/new"
                hx-target="#modal"
                hx-swap="innerHTML"
                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            New Task
        </button>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow p-4 mb-6">
        <div class="flex gap-4">
            <select name="status"
                    hx-get="/tasks"
                    hx-target="#task-list"
                    hx-swap="innerHTML"
                    hx-include="[name='priority'], [name='sort_by']"
                    class="border rounded px-3 py-2">
                <option value="">All Status</option>
                <option value="PENDING" {% if filters.status == 'PENDING' %}selected{% endif %}>Pending</option>
                <option value="COMPLETED" {% if filters.status == 'COMPLETED' %}selected{% endif %}>Completed</option>
            </select>

            <select name="priority"
                    hx-get="/tasks"
                    hx-target="#task-list"
                    hx-swap="innerHTML"
                    hx-include="[name='status'], [name='sort_by']"
                    class="border rounded px-3 py-2">
                <option value="">All Priority</option>
                <option value="HIGH" {% if filters.priority == 'HIGH' %}selected{% endif %}>High</option>
                <option value="MEDIUM" {% if filters.priority == 'MEDIUM' %}selected{% endif %}>Medium</option>
                <option value="LOW" {% if filters.priority == 'LOW' %}selected{% endif %}>Low</option>
            </select>

            <select name="sort_by"
                    hx-get="/tasks"
                    hx-target="#task-list"
                    hx-swap="innerHTML"
                    hx-include="[name='status'], [name='priority']"
                    class="border rounded px-3 py-2">
                <option value="display_order" {% if filters.sort_by == 'display_order' %}selected{% endif %}>Custom Order</option>
                <option value="due_date" {% if filters.sort_by == 'due_date' %}selected{% endif %}>Due Date</option>
                <option value="priority" {% if filters.sort_by == 'priority' %}selected{% endif %}>Priority</option>
            </select>
        </div>
    </div>

    <!-- Task List -->
    <div id="task-list" class="space-y-3">
        {% include 'tasks/_task_list.html' %}
    </div>
</div>

<!-- Modal container -->
<div id="modal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"></div>
{% endblock %}

{% block extra_body %}
<script>
// Initialize Sortable.js for drag-and-drop
document.addEventListener('DOMContentLoaded', function() {
    const taskList = document.getElementById('task-list');
    if (taskList) {
        new Sortable(taskList, {
            handle: '.drag-handle',
            onEnd: function(evt) {
                // Get new order of task IDs
                const taskIds = Array.from(taskList.children).map(
                    el => el.dataset.taskId
                );

                // Send reorder request
                fetch('/tasks/reorder', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({task_ids: taskIds})
                });
            }
        });
    }
});
</script>
{% endblock %}
```

### Task List Partial (`templates/tasks/_task_list.html`)
```html
{% for task in tasks %}
    {% include 'tasks/_task.html' %}
{% empty %}
    <div class="text-center text-gray-500 py-8">
        <p>No tasks found. <a href="/tasks/new" class="text-blue-500 hover:underline">Create your first task</a></p>
    </div>
{% endfor %}
```

### Single Task Component (`templates/tasks/_task.html`)
```html
<div class="bg-white rounded-lg shadow p-4 task-item"
     data-task-id="{{ task.id }}"
     data-priority="{{ task.priority.value }}"
     data-status="{{ task.status.value }}">

    <div class="flex items-center gap-3">
        <!-- Drag handle -->
        <div class="drag-handle cursor-move text-gray-400">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 4a1 1 0 011-1h.01a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h.01a1 1 0 110 2H4a1 1 0 01-1-1zM3 16a1 1 0 011-1h.01a1 1 0 110 2H4a1 1 0 01-1-1zM8 4a1 1 0 011-1h8a1 1 0 110 2H9a1 1 0 01-1-1zM8 10a1 1 0 011-1h8a1 1 0 110 2H9a1 1 0 01-1-1zM8 16a1 1 0 011-1h8a1 1 0 110 2H9a1 1 0 01-1-1z"></path>
            </svg>
        </div>

        <!-- Completion checkbox -->
        <input type="checkbox"
               {% if task.status.value == 'COMPLETED' %}checked{% endif %}
               hx-put="/tasks/{{ task.id }}/toggle"
               hx-target="closest .task-item"
               hx-swap="outerHTML"
               class="rounded">

        <!-- Task content -->
        <div class="flex-1 {% if task.status.value == 'COMPLETED' %}line-through text-gray-500{% endif %}">
            <div class="flex items-center justify-between">
                <h3 class="font-semibold">{{ task.title }}</h3>
                <div class="flex items-center gap-2">
                    <!-- Priority badge -->
                    <span class="px-2 py-1 text-xs rounded
                           {% if task.priority.value == 'HIGH' %}bg-red-100 text-red-800
                           {% elif task.priority.value == 'MEDIUM' %}bg-yellow-100 text-yellow-800
                           {% else %}bg-green-100 text-green-800{% endif %}">
                        {{ task.priority.value }}
                    </span>

                    <!-- Due date -->
                    {% if task.due_date %}
                    <span class="text-sm text-gray-600">
                        Due: {{ task.due_date.strftime('%m/%d/%Y') }}
                    </span>
                    {% endif %}
                </div>
            </div>

            {% if task.description %}
            <p class="text-gray-600 mt-1">{{ task.description }}</p>
            {% endif %}
        </div>

        <!-- Actions -->
        <div class="flex gap-2">
            <button hx-get="/tasks/{{ task.id }}/edit"
                    hx-target="#modal"
                    hx-swap="innerHTML"
                    class="text-blue-500 hover:text-blue-700">
                Edit
            </button>
            <button hx-delete="/tasks/{{ task.id }}"
                    hx-target="closest .task-item"
                    hx-swap="outerHTML"
                    hx-confirm="Are you sure you want to delete this task?"
                    class="text-red-500 hover:text-red-700">
                Delete
            </button>
        </div>
    </div>
</div>
```

### Task Form Template (`templates/tasks/_form.html`)
```html
<div class="bg-white rounded-lg p-6 max-w-md mx-auto">
    <h3 class="text-lg font-semibold mb-4">
        {% if task %}Edit Task{% else %}New Task{% endif %}
    </h3>

    <form {% if task %}
            hx-put="/tasks/{{ task.id }}"
          {% else %}
            hx-post="/tasks"
          {% endif %}
          hx-target="#task-list"
          hx-swap="innerHTML">

        <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Title</label>
            <input type="text"
                   name="title"
                   value="{{ task.title if task else '' }}"
                   required
                   maxlength="200"
                   class="w-full border rounded px-3 py-2">
        </div>

        <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Description</label>
            <textarea name="description"
                      maxlength="1000"
                      rows="3"
                      class="w-full border rounded px-3 py-2">{{ task.description if task else '' }}</textarea>
        </div>

        <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Due Date</label>
            <input type="datetime-local"
                   name="due_date"
                   value="{{ task.due_date.strftime('%Y-%m-%dT%H:%M') if task and task.due_date else '' }}"
                   class="w-full border rounded px-3 py-2">
        </div>

        <div class="mb-6">
            <label class="block text-sm font-medium mb-2">Priority</label>
            <select name="priority" class="w-full border rounded px-3 py-2">
                <option value="LOW" {% if task and task.priority.value == 'LOW' %}selected{% endif %}>Low</option>
                <option value="MEDIUM" {% if task and task.priority.value == 'MEDIUM' %}selected{% endif %}>Medium</option>
                <option value="HIGH" {% if task and task.priority.value == 'HIGH' %}selected{% endif %}>High</option>
            </select>
        </div>

        <div class="flex gap-3">
            <button type="submit"
                    class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                {% if task %}Update{% else %}Create{% endif %}
            </button>
            <button type="button"
                    onclick="document.getElementById('modal').classList.add('hidden')"
                    class="bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400">
                Cancel
            </button>
        </div>
    </form>
</div>
```

## HTMX Interaction Patterns

### API Route Behavior
Each route should handle multiple response types:

```python
@app.get("/tasks")
async def list_tasks(request: Request, ...):
    tasks = await task_service.get_tasks(...)

    # For HTMX partial updates
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            "tasks/_task_list.html",
            {"request": request, "tasks": tasks}
        )

    # For full page loads
    return templates.TemplateResponse(
        "tasks/list.html",
        {"request": request, "tasks": tasks, "filters": filters}
    )
```

### Modal Handling
```python
@app.get("/tasks/new")
async def new_task_form(request: Request):
    return templates.TemplateResponse(
        "tasks/_form.html",
        {"request": request}
    )

@app.get("/tasks/{task_id}/edit")
async def edit_task_form(request: Request, task_id: UUID):
    task = await task_service.get_task(task_id)
    return templates.TemplateResponse(
        "tasks/_form.html",
        {"request": request, "task": task}
    )
```

This template specification provides concrete implementation details that can be directly referenced during the task execution phase.