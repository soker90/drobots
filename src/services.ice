// -*- mode:c++ -*-
#include "drobots.ice"

module Services {
  exception AlreadyExists { string key; };
  exception NoSuchKey { string key; };

  dictionary<string, Object*> ObjectPrxDict;

  interface Container {
    void link(string key, Object* proxy) throws AlreadyExists;
    void unlink(string key) throws NoSuchKey;
    ObjectPrxDict list();
  };

  interface Factory {
    drobots::RobotController* make(drobots::Robot* bot);
    drobots::DetectorController makeDetectorController();
  };
};
