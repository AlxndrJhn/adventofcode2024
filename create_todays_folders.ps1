# if the first argument is a number, use that as the day number, with leading 0
# otherwise, use today's date
if ($args[0] -match "^\d+$") {
    $todayAsNumNoLeadingZero = $args[0].ToString()
}
else {
    $todayAsNumNoLeadingZero = (Get-Date).ToString("dd").TrimStart('0')
}
$todayAsPaddedNum = $todayAsNumNoLeadingZero.PadLeft(2, '0')

# copy template to new folder
Copy-Item -r template "$todayAsPaddedNum"

# fetch input from https://adventofcode.com/2024/day/9/input
code "$todayAsPaddedNum/day.py"
code "$todayAsPaddedNum/input_example.txt"
code "$todayAsPaddedNum/input.txt"

Start-Process firefox "https://adventofcode.com/2024/day/$todayAsNumNoLeadingZero"
Start-Process firefox "https://adventofcode.com/2024/day/$todayAsNumNoLeadingZero/input"
