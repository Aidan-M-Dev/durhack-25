CREATE OR REPLACE FUNCTION lecturers_from_module_iteration(module_iteration_id INT)
RETURNS TABLE (id INT, name VARCHAR)
LANGUAGE sql
AS $$
  SELECT 
    l.id,
    l.name
  FROM lecturers l
  INNER JOIN module_iterations_lecturers_links mil 
    ON l.id = mil.lecturer_id
  WHERE mil.module_iteration_id = module_iteration_id;
$$;