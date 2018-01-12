var selected = -1;

function deleteSelected(){
    if(selected >= 0)
    {
        return selected;
    }
}

function mark2select(workoutID) {
    selected = workoutID;
}
