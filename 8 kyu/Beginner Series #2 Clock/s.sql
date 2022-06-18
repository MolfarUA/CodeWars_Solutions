55f9bca8ecaa9eac7100004a


select (3600*h + 60*m + s)*1000 as res
from past;
__________________________
SELECT  ((h*60 + m)*60+ s )*1000 as res 

FROM past
__________________________
select h * 60 * 60 * 1000 + m * 60 * 1000 + s * 1000 as res from past
__________________________
select 1000*(s+60*(m+60*h)) as res from past
__________________________
CREATE FUNCTION to_milliseconds(h integer, m integer, s integer) RETURNS bigint
    LANGUAGE plpgsql
    IMMUTABLE
    AS $$
        BEGIN
            RETURN (h * 3600 + m * 60 + s) * 1000;
        END;
    $$;

SELECT to_milliseconds(h, m, s) AS res FROM past;
__________________________
select ((h*3600 + m*60 + s)* 1000 )as res 
from past
where (h between 0 and 23) and (m between 0 and 59) and (s between 0 and 59)
