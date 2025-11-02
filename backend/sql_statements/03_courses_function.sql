CREATE OR REPLACE FUNCTION courses_from_module_iteration(module_iteration_id INT)
RETURNS TABLE (id INT, home_department_id INT, title VARCHAR)
LANGUAGE sql
AS $$
  SELECT DISTINCT c.*
  FROM courses c
  INNER JOIN module_iterations_courses_links micl ON micl.course_id = c.id
  INNER JOIN module_iterations mi ON mi.id = micl.module_iteration_id
  WHERE mi.id = module_iteration_id;
$$;