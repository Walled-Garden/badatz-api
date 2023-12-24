SELECT item_id FROM public.test_item
WHERE (NLEVEL("test_item"."path") = 1 AND "test_item"."launch_id" = 1135)

-- select test_item.item_id, item_attribute.key
-- from test_item
-- inner join  item_attribute on item_attribute.item_id=test_item.item_id
-- WHERE (NLEVEL("test_item"."path") = 1 AND "test_item"."launch_id" = 1135)

select res.item_id, STRING_AGG(res.value, ', ') as value, STRING_AGG(res.key, ', ') as key
from (select test_item.item_id, item_attribute.value,item_attribute.key
from item_attribute
inner join  test_item on item_attribute.item_id=test_item.item_id
WHERE (NLEVEL("test_item"."path") = 1 AND "test_item"."launch_id" = 1135)
) as res
group by item_id


select test_item.item_id, item_attribute.value,item_attribute.key
from item_attribute
inner join  test_item on item_attribute.item_id=test_item.item_id
WHERE (NLEVEL("test_item"."path") = 1 AND "test_item"."launch_id" = 1135)


SELECT * FROM public.test_item
                    WHERE (NLEVEL("test_item"."path") = {_path} AND "test_item"."launch_id" = {_launch_id})


WITH "filtered" AS
	(SELECT "public"."test_item"."item_id" AS "id"
		FROM "public"."test_item"
		LEFT OUTER JOIN "public"."launch" ON "public"."test_item"."launch_id" = "public"."launch"."id"
		WHERE "test_item"."launch_id" = 1135
		GROUP BY "public"."test_item"."item_id"
		ORDER BY "test_item"."item_id" ASC
		LIMIT 10)
SELECT "public"."test_item"."item_id",
	"public"."test_item"."name",
	"public"."test_item"."code_ref",
	"public"."test_item"."type",
	"public"."test_item"."start_time",
	"public"."test_item"."description",
	"public"."test_item"."last_modified",
	"public"."test_item"."path",
	"public"."test_item"."unique_id",
	"public"."test_item"."uuid",
	"public"."test_item"."test_case_id",
	"public"."test_item"."test_case_hash",
	"public"."test_item"."parent_id",
	"public"."test_item"."retry_of",
	"public"."test_item"."has_children",
	"public"."test_item"."has_stats",
	"public"."test_item"."has_retries",
	"public"."test_item"."launch_id",
	"public"."test_item_results"."status",
	"public"."test_item_results"."end_time",
	"public"."test_item_results"."duration",
	"public"."item_attribute"."key",
	"public"."item_attribute"."value",
	"public"."item_attribute"."system",
	"public"."parameter"."item_id",
	"public"."parameter"."key",
	"public"."parameter"."value",
	"public"."statistics_field"."name",
	"public"."statistics"."s_counter",
	"public"."issue"."issue_id",
	"public"."issue"."auto_analyzed",
	"public"."issue"."ignore_analyzer",
	"public"."issue"."issue_description",
	"public"."issue_type"."locator",
	"public"."issue_type"."abbreviation",
	"public"."issue_type"."hex_color",
	"public"."issue_type"."issue_name",
	"public"."issue_group"."issue_group",
	"public"."ticket"."id",
	"public"."ticket"."bts_project",
	"public"."ticket"."bts_url",
	"public"."ticket"."ticket_id",
	"public"."ticket"."url",
	"public"."ticket"."plugin_name",
	"public"."pattern_template"."id",
	"public"."pattern_template"."name"
FROM "public"."test_item"
JOIN "filtered" ON "public"."test_item"."item_id" = "filtered"."id"
LEFT OUTER JOIN "public"."launch" ON "public"."test_item"."launch_id" = "public"."launch"."id"
LEFT OUTER JOIN "public"."test_item_results" ON "public"."test_item"."item_id" = "public"."test_item_results"."result_id"
LEFT OUTER JOIN "public"."item_attribute" ON "public"."test_item"."item_id" = "public"."item_attribute"."item_id"
LEFT OUTER JOIN "public"."statistics" ON "public"."test_item"."item_id" = "public"."statistics"."item_id"
LEFT OUTER JOIN "public"."statistics_field" ON "public"."statistics"."statistics_field_id" = "public"."statistics_field"."sf_id"
LEFT OUTER JOIN "public"."pattern_template_test_item" ON "public"."test_item"."item_id" = "public"."pattern_template_test_item"."item_id"
LEFT OUTER JOIN "public"."pattern_template" ON "public"."pattern_template_test_item"."pattern_id" = "public"."pattern_template"."id"
LEFT OUTER JOIN "public"."issue" ON "public"."test_item_results"."result_id" = "public"."issue"."issue_id"
LEFT OUTER JOIN "public"."issue_type" ON "public"."issue"."issue_type" = "public"."issue_type"."id"
LEFT OUTER JOIN "public"."issue_group" ON "public"."issue_type"."issue_group_id" = "public"."issue_group"."issue_group_id"
LEFT OUTER JOIN "public"."issue_ticket" ON "public"."issue"."issue_id" = "public"."issue_ticket"."issue_id"
LEFT OUTER JOIN "public"."ticket" ON "public"."issue_ticket"."ticket_id" = "public"."ticket"."id"
LEFT OUTER JOIN "public"."parameter" ON "public"."test_item"."item_id" = "public"."parameter"."item_id"
LEFT OUTER JOIN "public"."item_attribute" AS "launchAttribute" ON "public"."launch"."id" = "launchAttribute"."launch_id"
LEFT OUTER JOIN "public"."clusters_test_item" ON "public"."test_item"."item_id" = "public"."clusters_test_item"."item_id"
ORDER BY "test_item"."item_id" ASC