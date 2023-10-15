#!/usr/bin/python3
"""Class Declaration  HBnB console."""
from shlex import split
from ast import literal_eval
import cmd
import re
from models import storage


def parse(arg):
    """Fucntion that parsing our regulur expresion"""
    braces = re.search(r"\{(.*?)\}", arg)
    braket = re.search(r"\[(.*?)\]", arg)
    if braces is None:
        if braket is None:
            return [j.strip(",") for j in split(arg)]
        else:
            rex = split(arg[:braket.span()[0]])
            retr = [j.strip(",") for j in rex]
            retr.append(braket.group())
            return retr
    else:
        rex = split(arg[:braces.span()[0]])
        retr = [j.strip(",") for j in rex]
        retr.append(braces.group())
        return retr


class HBNBCommand(cmd.Cmd):
    """initialization  HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

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

    def emptyline(self):
        """Empty line."""

    def default(self, arg: str):
        """Default Fuction"""
        argment_dict = {
            "do_all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argregs = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argregs[1])
            if match is not None:
                command = [argregs[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argment_dict:
                    new_var = "{} {}"
                    cls = new_var.format(argregs[0], command[1])
                    return argment_dict[command[0]](cls)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to Terminate Application"""
        return True

    def do_eof(self, arg):
        """End Of File signal to Terminate Application"""
        print("")
        return True

    def do_create(self, arg):
        """create a new class instance """

        argregs = parse(arg)
        if len(argregs) == 0:
            print("** class name missing **")
        elif argregs[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(literal_eval(argregs[0])().id)
            storage.save()

    def do_show(self, arg):
        """Display  class instance """
        argregs = parse(arg)
        object_dict = storage.all()
        new_var1 = "{}.{}"
        if len(argregs) == 0:
            print("** class name missing **")
        elif argregs[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argregs) == 1:
            print("** instance id missing **")
        elif new_var1.format(argregs[0], argregs[1]) not in object_dict:
            print("** no instance found **")
        else:
            new_var = "{}.{}"
            print(object_dict[new_var.format(argregs[0], argregs[1])])

    def do_destroy(self, arg):
        """Delete a class instance """
        argregs = parse(arg)
        object_dict = storage.all()
        new_var = "{}.{}"
        if len(argregs) == 0:
            print("** class name missing **")
        elif argregs[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argregs) == 1:
            print("** instance id missing **")
        elif new_var.format(argregs[0], argregs[1]) not in object_dict:
            print("** no instance found **")
        else:
            new_var1 = "{}.{}"
            del object_dict[new_var1.format(argregs[0], argregs[1])]
            storage.save()

    def do_all(self, arg):
        """ Display  all instances """
        argregs = parse(arg)
        if len(argregs) > 0 and argregs[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            object_list = []
            for obj in storage.all().values():
                if len(argregs) > 0 and argregs[0] == obj.__class__.__name__:
                    object_list.append(str(obj))
                elif len(argregs) == 0:
                    object_list.append(str(obj))
            print(object_list)

    def do_count(self, arg):
        """Count  number of instances """
        argregs = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argregs[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """ Update  instance of a given  Class """
        argregs = parse(arg)
        object_dict = storage.all()

        if len(argregs) == 0:
            print("** class name missing **")
            return False
        if argregs[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argregs) == 1:
            print("** instance id missing **")
            return False
        new_var2 = object_dict.keys()
        new_var3 = "{}.{}"
        if new_var3.format(argregs[0], argregs[1]) not in new_var2:
            print("** no instance found **")
            return False
        if len(argregs) == 2:
            print("** attribute name missing **")
            return False
        if len(argregs) == 3:
            try:
                isinstance(literal_eval(argregs[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argregs) == 4:
            new_var1 = "{}.{}"
            obj = object_dict[new_var1.format(argregs[0], argregs[1])]
            if argregs[2] in obj.__class__.__dict__.keys():
                valtype = isinstance(obj.__class__.__dict__[argregs[2]])
                obj.__dict__[argregs[2]] = valtype(argregs[3])
            else:
                obj.__dict__[argregs[2]] = argregs[3]
        elif isinstance(literal_eval(argregs[2])) == dict:
            new_var = "{}.{}"
            obj = object_dict[new_var.format(argregs[0], argregs[1])]
            for k, v in literal_eval(argregs[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = isinstance(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
