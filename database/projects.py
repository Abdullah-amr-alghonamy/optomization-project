import json

from database.db import get_connection


def create_project(user_id, project_name):
    """Create a new project for a user."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO projects (
            user_id,
            project_name,
            current_stage,
            data
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            project_name,
            "setup",
            json.dumps({})
        )
    )

    project_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return project_id


def save_project(user_id, project_id, data, current_stage):
    """Save/update a project's data and current stage."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE projects
        SET
            data = ?,
            current_stage = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE
            id = ?
            AND user_id = ?
        """,
        (
            json.dumps(data),
            current_stage,
            project_id,
            user_id
        )
    )

    conn.commit()
    conn.close()


def load_project(user_id, project_id):
    """Load a project belonging to a specific user."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            project_name,
            current_stage,
            data,
            created_at,
            updated_at
        FROM projects
        WHERE
            id = ?
            AND user_id = ?
        """,
        (
            project_id,
            user_id
        )
    )

    project = cursor.fetchone()

    conn.close()

    if project is None:
        return None

    return {
        "id": project["id"],
        "project_name": project["project_name"],
        "current_stage": project["current_stage"],
        "data": json.loads(project["data"]),
        "created_at": project["created_at"],
        "updated_at": project["updated_at"]
    }


def list_projects(user_id):
    """Return all projects belonging to a specific user."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            project_name,
            current_stage,
            created_at,
            updated_at
        FROM projects
        WHERE user_id = ?
        ORDER BY updated_at DESC
        """,
        (user_id,)
    )

    projects = cursor.fetchall()

    conn.close()

    return [dict(project) for project in projects]


def delete_project(user_id, project_id):
    """Delete a project belonging to a specific user."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM projects
        WHERE
            id = ?
            AND user_id = ?
        """,
        (
            project_id,
            user_id
        )
    )

    conn.commit()
    conn.close()