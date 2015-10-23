/**
 * Created by dulat on 23.09.14.
 */

var lock;
lock = false;

setInterval(
    function(collback){
    if (!lock)
    {
        badge_json();
        lock = true;}},
    5000
)