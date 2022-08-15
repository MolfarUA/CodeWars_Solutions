52742f58faf5485cae000b9a


function format_duration($seconds)
{

$data = [
  'second'=> floor($seconds) % 60,
  'minute'=> floor($seconds / 60) % 60,
  'hour'  => floor($seconds / (60 * 60)) % 24,
  'day'   => floor($seconds / (60 * 60 * 24)) % 365,
  //'month' => floor($seconds / (60 * 60 * 24 * 30)) % 12,
  'year'  => floor($seconds / (60 * 60 * 24 * 365)),
];

$result = '';
foreach ($data as $key => $interval)
{
  if($interval != 0) {
    $tmp = $interval.' '.$key.($interval > 1 ? 's' : '');
    $result = empty($result) ? $tmp : $tmp.', '.$result;
  }
}

return empty($result) ? 'now' : str_lreplace(',', ' and', $result);
}
    
function str_lreplace($search, $replace, $subject){
    $pos = strrpos($subject, $search);
    if($pos !== false)    {
        $subject = substr_replace($subject, $replace, $pos, strlen($search));
    }
    return $subject;
}

__________________________________________________
function format_duration($seconds)
{
    if ($seconds < 0) {
        return null;
    }
    if ($seconds === 0) {
        return 'now';
    }

    $periods = [
        'year'   => 60 * 60 * 24 * 365,
        'day'    => 60 * 60 * 24,
        'hour'   => 60 * 60,
        'minute' => 60,
        'second' => 1,
    ];
    $result = [];
    $count = 0;
    foreach ($periods as $key => $period) {
        $t = intdiv($seconds, $period);
        if ($t > 0) {
            $result[] = ($t > 1) ? "$t {$key}s" : "$t $key";
            $count++;
        }
        $seconds %= $period;
    }
    if ($count > 1) {
        $result[$count - 2] .= ' and ' . array_pop($result);
    }
    return implode(', ', $result);
}
      
__________________________________________________
function format_duration($s){
  return (new HumanReadableTimeFormatter())->format($s);
}

/**
 * Format a time given in seconds in a human readable format
 */
class HumanReadableTimeFormatter
{

    /**
     * Initialize formatter
     *
     * @param Unit[]    $unitsOfTime the units to be used for formatting
     */
    public function __construct(array $unitsOfTime = null)
    {
        if ($unitsOfTime) {
            $this->unitsOfTime = $unitsOfTime;
        } else {
            $this->unitsOfTime = self::getDefaultUnitsOfTime();
        }

        // Order unitsOfTime from largest to smallest
        usort($this->unitsOfTime, function($a, $b) {
            return $b->amountOfSeconds - $a->amountOfSeconds;
        });
    }

    /**
     * @return Unit[]
     */
    public static function getDefaultUnitsOfTime() : array
    {
        $second = new Unit(1, 'second');
        $minute = $second->getMultiple(60, 'minute');
        $hour = $minute->getMultiple(60, 'hour');
        $day = $hour->getMultiple(24, 'day');
        $year = $day->getMultiple(365, 'year');
        return [$year, $day, $hour, $minute, $second];
    }

    /**
     * @param int $seconds  Amount of time in seconds to format
     * @return string       Formatted amount of time
     */
    public function format(int $seconds) : string
    {
        if ($seconds == 0) {
            return "now";
        }
        $amounts = $this->extractUnitsOfTime($seconds);
        return $this->concatAmounts($amounts);
    }

    /**
     * Splits time in seconds into specified Units of time
     * @param int $seconds Time span in seconds
     * @return Amount[]
     */
    private function extractUnitsOfTime(int $seconds) : array
    {
        $amounts = [];
        foreach ($this->unitsOfTime as $unit) {
            $rest = $seconds % $unit->amountOfSeconds;
            $amount = ($seconds - $rest) / $unit->amountOfSeconds;
            if($amount > 0){
                $amounts[] = new Amount($amount, $unit);
            }
            $seconds = $rest;
        }
        return $amounts;
    }

    /**
     * Concatenates Amounts with human readable delimiters.
     * @param Amount[] $amounts
     * @return string
     */
    private function concatAmounts(array $amounts) : string
    {
        if (count($amounts) == 1) {
            return (string)$amounts[0];
        }
        $last = array_pop($amounts);
        return implode($amounts, ", ") . " and " . $last;
    }
}

/**
 * A Unit of time, such as a minute, day or month
 */
class Unit
{

    /**
     * @param type $amountOfSeconds Conversion factor between this unit and a second
     * @param type $label           Label of this unit
     */
    public function __construct(int $amountOfSeconds, string $label)
    {
        $this->amountOfSeconds = $amountOfSeconds;
        $this->label = $label;
    }

    /**
     *
     * @param int    $multiple    Multiplication factor between this unit and the new one
     * @param string $label       Label of the new Unit
     * @return \Unit              New Unit
     */
    public function getMultiple(int $multiple, string $label) : Unit
    {
        return new Unit($this->amountOfSeconds * $multiple, $label);
    }

    /**
     * @param boolean $plural  Indicates whether the unit name shall be inflected for plural.
     * @return string          Formatted unit label
     */
    public function formatLabel(bool $plural = false) : string
    {
        return $this->label . ($plural ? "s" : "");
    }
}

/**
 * Used to store an amount and corresponding Unit
 */
class Amount
{

    /**
     *
     * @param int  $amount
     * @param Unit $unit
     */
    public function __construct(int $amount, Unit $unit)
    {
        $this->amount = $amount;
        $this->unit = $unit;
    }

    public function __toString() : string
    {
        return $this->amount . " " .$this->unit->formatLabel($this->amount > 1);
    }
}
