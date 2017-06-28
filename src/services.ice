// -*- mode:c++ -*-
#include "drobots.ice"

module Services {
  exception AlreadyExists { string key; };
  exception NoSuchKey { string key; };

  dictionary<string, Object*> ObjectPrxDict;

  interface Container {
    void link(string key, Object* proxy) throws AlreadyExists;
    void linkFactory(string key, Object* proxy) throws AlreadyExists;
    void linkController(string key, Object* proxy) throws AlreadyExists;
    void unlink(string key) throws NoSuchKey;
    ObjectPrxDict list();
    ObjectPrxDict listFactory();
    ObjectPrxDict listController();
  };

  interface Factory {
    drobots::RobotController* make(drobots::Robot* bot, int index);
    drobots::DetectorController* makeDetector(int index);
  };
};
