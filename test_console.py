#!/usr/bin/python3
import cmd
import re
from shlex import split

import models
from models import storage

import tests
from tests.test_models.test_base_model import BaseModel
from tests.test_models.test_user import User
from tests.test_models.test_city import City
from tests.test_models.test_amenity import Amenity
from tests.test_models.test_place import Place
from tests.test_models.test_state import State
from tests.test_models.test_review import Review

def parse(argmt):
    curly_match = re.search(r"\{(.*?)\}", argmt)
    bracket_match = re.search(r"\[(.*?)\]", argmt)
    if curly_match is None:
        if bracket_match is None:
            return [item.strip(",") for item in argmt.split()]
        else:
            split_val = argmt[:bracket_match.span()[0]].split()
            result_list = [item.strip(",") for item in split_val]
            result_list.append(bracket_match.group())
            return result_list
    else:
        split_val = argmt[:curly_match.span()[0]].split()
        result_list = [item.strip(",") for item in split_val]
        result_list.append(curly_match.group())
        return result_list


class HBNBCommand(cmd.Cmd):
    """prompt command to be displayed on the console"""
    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            arg_search = [arg[:match.span()[0]], arg[match.span()[1]:]]
            matched_arg = re.search(r"\((.*?)\)", arg_search[1])
            if match is not None:
                command_exc = [arg_search[1][:matched_arg.span()[0]],
                               matched_arg.group()[1:-1]]
                if command_exc[0] in argdict.keys():
                    call = "{} {}".format(arg_search[0], command_exc[1])
                    return argdict[command_exc[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print("")  # Print a new line before exiting
        return True

    def emptyline(self):
        """Handle empty line and do  nothing """
        pass

    def do_create(self, arg):
        """Create a new instance of a model"""
        parses_arg = parse(arg)
        if len(parses_arg) == 0:
            print("** class name missing **")
        elif parses_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(parses_arg[0])().id)
            storage.save()

    def do_show(self, arg):
        """Show details of a model instance"""
        parsed_arg = parse(arg)
        object_dict = storage.all()
        if len(parsed_arg) == 0:
            print("** class name missing **")
        elif parsed_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(parsed_arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(parsed_arg[0], parsed_arg[1]) not in object_dict:
            print("** no instance found **")
        else:
            print(object_dict["{}.{}".format(parsed_arg[0], parsed_arg[1])])

    def do_destroy(self, arg):
        """Delete a model instance"""
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in globals():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key in storage.all():
                storage.all().pop(key)
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """Show all instances of a model"""
        par_arg = parse(arg)
        if len(par_arg) > 0 and par_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(par_arg) > 0 and par_arg[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(par_arg) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def do_update(self, arg):
        """Update attributes of a model instance"""
        parsed_arg = parse(arg)
        obj_dict = storage.all()

        if len(parsed_arg) == 0:
            print("** class name missing **")
            return False
        if parsed_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(parsed_arg) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(parsed_arg[0], parsed_arg[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(parsed_arg) == 2:
            print("** attribute name missing **")
            return False
        if len(parsed_arg) == 3:
            try:
                type(eval(parsed_arg[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(parsed_arg) == 4:
            obj = obj_dict["{}.{}".format(parsed_arg[0], parsed_arg[1])]
            if parsed_arg[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[parsed_arg[2]])
                obj.__dict__[parsed_arg[2]] = valtype(parsed_arg[3])
            else:
                obj.__dict__[parsed_arg[2]] = parsed_arg[3]
        elif type(eval(parsed_arg[2])) == dict:
            obj = obj_dict["{}.{}".format(parsed_arg[0], parsed_arg[1])]
            for k, v in eval(parsed_arg[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_count(self, arg):
        """Count the number of instances of a model"""
        parsed_arg = parse(arg)
        count = 0
        for obj in storage.all().values():
            if parsed_arg[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_exit(self, arg):
        """Exit the program"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
