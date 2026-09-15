from database.projects import (
    create_project,
    save_project,
    load_project,
    list_projects
)


# هنستخدم user_id = 1 للاختبار
user_id = 1


# 1. Create project
project_id = create_project(
    user_id,
    "Test Optimization Project"
)

print("Created project ID:", project_id)


# 2. Save project data
test_data = {
    "temperature": 150,
    "pressure": 5,
    "concentration": 2.5
}

save_project(
    user_id,
    project_id,
    test_data,
    "screening"
)

print("Project saved successfully!")


# 3. Load project
project = load_project(
    user_id,
    project_id
)

print("\nLoaded project:")
print(project)


# 4. List user's projects
projects = list_projects(user_id)

print("\nAll projects:")
for p in projects:
    print(p)