58b1ae711fcffa34090000ea


public class Door {
    public static String run(String events) {
    
        int state = 0, dir = 1;
        boolean moving = false;
        StringBuilder out = new StringBuilder();
        
        for (int n = 0 ; n < events.length() ; n++) {
            char c = events.charAt(n);
            
            if (c == 'O')         dir *= -1;
            else if (c == 'P')    moving = !moving;
            if (moving)           state += dir;
            if (state % 5 == 0) {
                moving = false;
                dir = state == 0 ? 1 : -1;
            }
            out.append(state);
        }
        return out.toString();
    }
}
______________________________________
public class Door {

    private interface State {

        void onNoEvent(Door door);

        void onButtonPressed(Door door);

        void onObstacleDetected(Door door);

    }

    private class Open implements State {

        @Override
        public void onNoEvent(Door door) {

        }

        @Override
        public void onButtonPressed(Door door) {
            door.decreaseOpeningLevel();
            door.changeState(new Closing());
        }

        @Override
        public void onObstacleDetected(Door door) {

        }

    }

    private class Closed implements State {

        @Override
        public void onNoEvent(Door door) {

        }

        @Override
        public void onButtonPressed(Door door) {
            door.increaseOpeningLevel();
            door.changeState(new Opening());
        }

        @Override
        public void onObstacleDetected(Door door) {

        }

    }

    private class Opening implements State {

        @Override
        public void onNoEvent(Door door) {
            if (door.isCompletelyOpen())
                door.changeState(new Open());
            else
                door.increaseOpeningLevel();
        }

        @Override
        public void onButtonPressed(Door door) {
            door.changeState(new PausedWhileOpening());
        }

        @Override
        public void onObstacleDetected(Door door) {
            door.decreaseOpeningLevel();
            door.changeState(new Closing());
        }

    }

    private class Closing implements State {

        @Override
        public void onNoEvent(Door door) {
            if (door.isCompletelyClosed())
                door.changeState(new Closed());
            else
                door.decreaseOpeningLevel();
        }

        @Override
        public void onButtonPressed(Door door) {
            door.changeState(new PausedWhileClosing());
        }

        @Override
        public void onObstacleDetected(Door door) {
            door.increaseOpeningLevel();
            door.changeState(new Opening());
        }

    }

    private class PausedWhileOpening implements State {

        @Override
        public void onNoEvent(Door door) {

        }

        @Override
        public void onButtonPressed(Door door) {
            door.increaseOpeningLevel();
            door.changeState(new Opening());
        }

        @Override
        public void onObstacleDetected(Door door) {

        }

    }

    private class PausedWhileClosing implements State {

        @Override
        public void onNoEvent(Door door) {

        }

        @Override
        public void onButtonPressed(Door door) {
            door.decreaseOpeningLevel();
            door.changeState(new Closing());
        }

        @Override
        public void onObstacleDetected(Door door) {

        }

    }

    private State state;
    private int openingLevel;
    private StringBuilder openingLevelHistory;

    public Door() {
        state = new Closed();
        openingLevel = 0;
        openingLevelHistory = new StringBuilder();
    }

    public void changeState(State state) {
        this.state = state;
    }

    public void increaseOpeningLevel() {
        openingLevel++;
    }

    public void decreaseOpeningLevel() {
        openingLevel--;
    }

    public boolean isCompletelyOpen() {
        return openingLevel == 5;
    }

    public boolean isCompletelyClosed() {
        return openingLevel == 0;
    }

    public void saveOpeningLevel() {
        openingLevelHistory.append(openingLevel);
    }

    public String getOpeningLevelHistory() {
        return openingLevelHistory.toString();
    }

    private void testBehaviour(String events) {
        events.chars().forEach(event -> nextEvent((char)event));
    }

    private void nextEvent(char event) {
        switch (event) {
            case '.':
                state.onNoEvent(this);
                break;
            case 'P':
                state.onButtonPressed(this);
                break;
            case 'O':
                state.onObstacleDetected(this);
                break;
        }

        saveOpeningLevel();
    }

    public static String run(String events) {
        Door door = new Door();
        door.testBehaviour(events);
        return door.getOpeningLevelHistory();
    }

}
