SELECT
  sp.SalesPersonID AS salesperson_id,
  e.Title AS title,
  e.ContactID AS contact_id,
  e.LoginID AS login_id,
  st.Name AS territory
FROM adventureworks.salesperson sp
JOIN adventureworks.employee e ON sp.SalesPersonID = e.EmployeeID
LEFT JOIN adventureworks.salesterritory st ON sp.TerritoryID = st.TerritoryID;
