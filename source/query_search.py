parent_query = """
WITH items_union AS(
    Select
        temp.item_number,
        title,
        description,
        game_condition,
        game_type,
        email
    from
        Item AS it
        INNER JOIN (
            (
                select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Video game" as game_type,
                    email
                from
                    VideoGame
            )
            UNION
            (
                Select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Computer game" as game_type,
                    email
                from
                    ComputerGame
            )
            UNION
            (
                Select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Collectible card game" as game_type,
                    email
                from
                    CollectibleCardGame
            )
            UNION
            (
                select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Playing card game" as game_type,
                    email
                from
                    PlayingCardGame
            )
            UNION
            (
                select
                    item_number,
                    title,
                    description,
                    game_condition,
                    "Board game" as game_type,
                    email
                from
                    BoardGame
            )
        ) AS temp ON temp.item_number = it.item_number
),
query_on_user AS(
    -- Used to get logged in TradePlazaUser's email
    SELECT
        u.*
    FROM
        TradePlazaUser u
    WHERE
        u.email = '{user_email}'
),
accepted_trade_items AS (
    -- Used to get list of accepted items (proposer and counterparty) so that we can exclude them
    SELECT
        proposer_item_number,
        counter_party_item_number,
        trade_status
    FROM
        Trade s
),
items_to_find_dist AS(
    SELECT
        item_number,
        game_type,
        title,
        game_condition,
        description,
        u.postal_code AS item_postal_code,
        u.email
    FROM
        items_union i
        LEFT JOIN TradePlazaUser u ON i.email = u.email
    WHERE
        u.email <> '{user_email}'
        AND item_number NOT IN(
            (
                SELECT
                    proposer_item_number
                FROM
                    accepted_trade_items
            )
            UNION
            (
                SELECT
                    counter_party_item_number
                FROM
                    accepted_trade_items
            )
        )
),
response_time AS(
    select
        i.email,
        ROUND(avg(DATEDIFF(NOW(),accept_reject_date)),1) as Response_Time
    From
        items_union i
        INNER JOIN TradePlazaUser u ON i.email = u.email
        INNER JOIN Trade tr on i.item_number = tr.counter_party_item_number
    where
        trade_status = 'ACCEPT'
        or trade_status = 'REJECT'
    Group By
        i.email
),
user_rank AS(
select email,
CASE
            WHEN trade_count >= 10 THEN 'Alexandinium'
            WHEN trade_count >= 8
            AND trade_count <= 9 THEN 'Platinum'
            WHEN trade_count >= 6
            AND trade_count <= 7 THEN 'Gold'
            WHEN trade_count >= 4
            AND trade_count <= 5 THEN 'Silver'
            WHEN trade_count >= 3
            AND trade_count <= 4 THEN 'Bronze'
            WHEN trade_count >= 1
            AND trade_count <= 2 THEN 'Aluminium'
        END as user_rank
        From
    (select
        i.email,
        Count(*) as trade_count
    From
        items_union i
        INNER JOIN TradePlazaUser u ON i.email = u.email
        INNER JOIN (
            (
                SELECT
                    proposer_item_number as tr_item_no
                FROM
                    accepted_trade_items
                where
                    trade_status = 'ACCEPT'
            )
            UNION
            (
                SELECT
                    counter_party_item_number as tr_item_no
                FROM
                    accepted_trade_items
                where
                    trade_status = 'ACCEPT'
            )
        ) tr on i.item_number = tr.tr_item_no
    Group By
        i.email
) as temp_rank ),
lat_lon AS(
    SELECT
        items_to_find_dist.*,
        response_time.Response_Time,
        user_rank.user_rank,
        query_on_user.postal_code AS user_postal_code,
        RADIANS(a.latitude) AS lat1,
        RADIANS(a2.latitude) AS lat2,
        RADIANS(a.longitude) AS lon1,
        RADIANS(a2.longitude) AS lon2,
        CAST(RADIANS(a2.latitude - a.latitude) AS DECIMAL(9,6))  AS delta_lat,
        CAST(RADIANS(a2.longitude - a.longitude) AS DECIMAL(9,6))AS delta_lon
    FROM
        items_to_find_dist
        LEFT JOIN response_time on items_to_find_dist.email = response_time.email
        LEFT JOIN user_rank on items_to_find_dist.email = user_rank.email
        CROSS JOIN query_on_user
        LEFT JOIN Address a ON items_to_find_dist.item_postal_code = a.postal_code
        LEFT JOIN Address a2 ON query_on_user.postal_code = a2.postal_code
),
haversine AS(
    SELECT
        DISTINCT  item_postal_code,
        user_postal_code,
        (SIN(delta_lat / 2.0) * SIN(delta_lat / 2.0)) + (
            COS(lat1) * COS(lat2) * SIN(delta_lon / 2.0) * SIN(delta_lon / 2.0)
        ) AS haversine_a
    FROM
        lat_lon
)
SELECT
    la.item_number,
    la.game_type,
    la.title,
    la.game_condition,
    la.description,
    la.Response_Time,
    la.user_rank,
    3958.75 * 2 * (ATAN2(SQRT(haversine_a), SQRT(1 - haversine_a))) AS distance
FROM
    lat_lon la
    LEFT JOIN haversine h ON (
        la.user_postal_code = h.user_postal_code
        AND la.item_postal_code = h.item_postal_code) {where_clause}
"""

def keyword_search(user_email, keyword):
    if "'" in keyword:
        i = keyword.index("'")
        keyword = keyword[0:i+1] + "'" + keyword[i+1:]

    where_clause = """WHERE
            LOWER(title) LIKE LOWER('%{keyword}%')
            OR LOWER(description) LIKE LOWER('%{keyword}%')
        ORDER BY
            distance ASC,
            item_number ASC""".format(keyword=keyword)

    query = parent_query.format(user_email=user_email,where_clause=where_clause)
    return query

def my_postal_search(user_email):

    where_clause= """
    WHERE h.item_postal_code = h.user_postal_code
    ORDER BY distance ASC, item_number ASC
    """
    query = parent_query.format(user_email=user_email,where_clause=where_clause)
    return query

def in_postal_search(user_email, postal_code):
    where_clause = """
    WHERE h.item_postal_code = '{postal_code}'
    ORDER BY distance ASC, item_number ASC
    """.format(postal_code=postal_code)

    query=parent_query.format(user_email=user_email,where_clause=where_clause)

    return query

def within_miles_search(user_email, miles):
    where_clause = """
    WHERE TRUNCATE(CAST((3958.75 * 2 * (ATAN2(SQRT(haversine_a), SQRT(1-haversine_a)))) As DECIMAL), 1) < {miles}
    ORDER BY distance ASC, item_number ASC
    """.format(miles=miles)

    query = parent_query.format(user_email=user_email,where_clause=where_clause)
    return query
