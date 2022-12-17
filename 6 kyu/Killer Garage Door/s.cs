58b1ae711fcffa34090000ea


using System;
public class Door
    {
        private static int FULLY_CLOSED = 0;
        private static int FULLY_OPEN = 5;
        private static char NO_EVENT = '.';
        private static char BUTTON_PRESSED = 'P';
        private static char OBSTACLE_DETECTED = 'O';
        private int currentposition = FULLY_CLOSED;
        private Status previousStatus = Status.idle;
        private Status currentStatus = Status.idle;
        private enum Status
        {
            idle = 0,
            up = 1,
            down = 2
        }

        public string ProcessEvents(string events)
        {
            var result = String.Empty;
            foreach(char currentEvent in events)
            {
                handleEvents(currentEvent);
                result += moveDoorByCurrentStatus();
                handleFullOpenFullClosedPositions();
            }
            return result;
        }
        private void handleEvents(char currentEvent)
        {
            if (currentEvent == OBSTACLE_DETECTED)
            {
                handleObstacle();
            }
            if (currentEvent == BUTTON_PRESSED)
            {
                handleButtonPress();
            }
            return;
        }
        private void handleFullOpenFullClosedPositions()
        {
            if(currentposition == FULLY_OPEN)
            {
                previousStatus = Status.up;
                currentStatus=Status.idle;
            }
            if(currentposition == FULLY_CLOSED) 
            {
                previousStatus = Status.down;
                currentStatus = Status.idle;
            }
        }
        private String moveDoorByCurrentStatus()
        {
            switch (this.currentStatus)
            {
                case Status.up: currentposition++; break;
                case Status.down: currentposition--; break;
            }
            return currentposition.ToString();
        }
        private void handleButtonPress()
        {
            // If the door is closed, a push starts opening the door, and vice-versa
            if (currentposition == FULLY_CLOSED)
            {
                currentStatus = Status.up;
                previousStatus = Status.idle;
                return;
            }
            if (currentposition == FULLY_OPEN)
            {
                currentStatus = Status.down;
                previousStatus = Status.idle;
                return;
            }
            // While the door is moving, one push pauses movement, another push resumes movement in the same direction
            if (currentStatus == Status.idle) {
                currentStatus = previousStatus;
             }
            else
            {
                previousStatus = currentStatus;
                currentStatus = Status.idle;
            }
            return;
        }
        private void handleObstacle()
        {
            switch (this.currentStatus) { 
                case Status.up:
                    currentStatus = Status.down;
                break;
                case Status.down:
                    currentStatus= Status.up;
                break;
            }
            return;
        }
    }
______________________________________
using System.Collections.Generic;
using System.Text;

public class Door
{
  private enum IncomingEvent
  {
    NoEvent,
    ButtonPressed,
    ObstacleDetected
  }
  
  private enum Direction
  {
    None,
    IsOpening,
    IsClosing
  }
  
  private class StateMachine
  {
    public int state()
    {
      return _currentState;
    }
    
    public void processInput(IncomingEvent e)
    {
      if (e == IncomingEvent.ButtonPressed)
      {
          if (isFullyClosed())
            {
              setCurrentState(1);
              _paused = false;
              return;
            }
          else if (isFullyOpen())
            {
              setCurrentState(4);
              _paused = false;
              return;
            }
          
          _paused = !_paused;
      }
      if (e == IncomingEvent.ObstacleDetected && !_paused)
      {
        if (_currentDirection == Direction.IsOpening)
        {
          _currentDirection = Direction.IsClosing;  
        }
        else if (_currentDirection == Direction.IsClosing)
        {
          _currentDirection = Direction.IsOpening;
        }
      }
    
      if (_currentDirection != Direction.None && !_paused)
      {
        if (_currentDirection == Direction.IsOpening)
        {
          setCurrentState(_currentState + 1);
        }
        else
        {
          setCurrentState(_currentState - 1);
        }
      }
    }
    
    private bool isFullyClosed()
    {
      return _currentState == 0;  
    }
    
    private bool isFullyOpen()
    {
      return _currentState == 5;  
    }
    
    private void setCurrentState(int state)
    {
      if (_currentState < state)
      {
        _currentDirection = Direction.IsOpening;  
      }
      else if (_currentState > state)
      {
        _currentDirection = Direction.IsClosing;
      }
      else
      {
        return;  
      }
      
      _currentState = state;
      
      if (isFullyClosed() || isFullyOpen())
      {
        _currentDirection = Direction.None;
      }
    }
    
    private Direction _currentDirection = Direction.None;
    private int _currentState = 0;
    private bool _paused = false;
  }
  
  public string ProcessEvents(string events)
  {
    var inputDictionary = new Dictionary<char, IncomingEvent>();
    inputDictionary.Add('.', IncomingEvent.NoEvent);
    inputDictionary.Add('P', IncomingEvent.ButtonPressed);
    inputDictionary.Add('O', IncomingEvent.ObstacleDetected);
    
    var stateMachine = new StateMachine();
    var resultBuilder = new StringBuilder();    
    foreach(char c in events)
    {
      stateMachine.processInput(inputDictionary[c]);
      resultBuilder.Append(stateMachine.state().ToString());
    }
    return resultBuilder.ToString();
  }
}
