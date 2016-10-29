// -*- mode:c++ -*-

module drobots {

  interface Player {
    string getID();
    void win();
    void lose();
  };

  exception InvalidProxy{};
  exception InvalidName{
    string reason;
  };

  interface Game {
    void login(Player* p, string nick)
      throws InvalidProxy, InvalidName;
    void loginSimple(string player, string nick)
      throws InvalidProxy, InvalidName;
  };
};