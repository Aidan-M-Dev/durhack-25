"""Database helper functions for module_guide."""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    """Create a new database connection."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def search_modules_by_code(module_code):
    """
    Search for modules by their code.

    Args:
        module_code (str): The module code to search for

    Returns:
        list: List of module dictionaries matching the code
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM modules WHERE code = %s", (module_code,))
    modules = cur.fetchall()

    cur.close()
    conn.close()

    return modules


def search_modules_by_name(search_term):
    """
    Search for modules by name using case-insensitive pattern matching.

    Args:
        search_term (str): The search term to match against module names

    Returns:
        list: List of module dictionaries matching the search term
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Use ILIKE for case-insensitive pattern matching
    search_pattern = f"%{search_term}%"
    cur.execute(
        "SELECT * FROM modules WHERE name ILIKE %s OR code ILIKE %s ORDER BY code",
        (search_pattern, search_pattern)
    )
    modules = cur.fetchall()

    cur.close()
    conn.close()

    return modules


def get_module_by_id(module_id):
    """
    Get a module by its ID.

    Args:
        module_id (int): The module ID

    Returns:
        dict: Module data or None if not found
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM modules WHERE id = %s", (module_id,))
    module = cur.fetchone()

    cur.close()
    conn.close()

    return module


def get_module_iterations(module_id):
    """
    Get all iterations of a module.

    Args:
        module_id (int): The module ID

    Returns:
        list: List of module iteration dictionaries
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM module_iterations WHERE module_id = %s", (module_id,))
    iterations = cur.fetchall()

    cur.close()
    conn.close()

    return iterations


def get_lecturers_for_iteration(module_iteration_id):
    """
    Get lecturers for a specific module iteration.

    Args:
        module_iteration_id (int): The module iteration ID

    Returns:
        list: List of lecturer dictionaries
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM lecturers_from_module_iteration(%s)", (module_iteration_id,))
    lecturers = cur.fetchall()

    cur.close()
    conn.close()

    return lecturers


def get_courses_for_iteration(module_iteration_id):
    """
    Get courses for a specific module iteration.

    Args:
        module_iteration_id (int): The module iteration ID

    Returns:
        list: List of course dictionaries
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM courses_from_module_iteration(%s)", (module_iteration_id,))
    courses = cur.fetchall()

    cur.close()
    conn.close()

    return courses


def get_published_reviews_for_iteration(module_iteration_id):
    """
    Get published reviews for a specific module iteration.

    Args:
        module_iteration_id (int): The module iteration ID

    Returns:
        list: List of review dictionaries
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "SELECT * FROM reviews WHERE module_iteration_id = %s AND moderation_status = %s",
        (module_iteration_id, 'published')
    )
    reviews = cur.fetchall()

    cur.close()
    conn.close()

    return reviews


def get_module_info_with_iterations(module_id):
    """
    Get complete module information including all iterations, lecturers, courses, and reviews.

    Args:
        module_id (int): The module ID

    Returns:
        dict: Dictionary with yearsInfo structure or None if module not found
    """
    module = get_module_by_id(module_id)

    if not module:
        return None

    iterations = get_module_iterations(module_id)

    years_info = {}
    for iteration in iterations:
        year = iteration['academic_year_start_year']
        term = iteration['term']

        lecturers = get_lecturers_for_iteration(iteration['id'])
        courses = get_courses_for_iteration(iteration['id'])
        reviews = get_published_reviews_for_iteration(iteration['id'])

        if year not in years_info:
            years_info[year] = {
                "term": term,
                "lecturers": lecturers,
                "courses": courses,
                "reviews": reviews
            }

    return years_info
