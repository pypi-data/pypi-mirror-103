import dis


def load_meths_attrs(i_meths, i_attrs, i_clsdict):
    for rec in i_clsdict:
        try:
            ret = dis.get_instructions(i_clsdict[rec])
        except TypeError:
            pass
        else:
            for re2 in ret:
                if re2.opname == 'LOAD_GLOBAL':
                    if re2.argval not in i_meths:
                        i_meths.append(re2.argval)
                elif re2.opname == 'LOAD_ATTR':
                    if re2.argval not in i_attrs:
                        i_attrs.append(re2.argval)
    #print(i_meths)
    #print(i_attrs)


class ServerVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        l_meths = []
        l_attrs = []

        load_meths_attrs(l_meths, l_attrs, clsdict)

        if 'connect' in l_meths:
            raise TypeError('Использование метода connect недопустимо в серверном классе')

        if not ('SOCK_STREAM' in l_attrs and 'AF_INET' in l_attrs):
            raise TypeError('Некорректная инициализация сокета.')

        super().__init__(clsname, bases, clsdict)

class ClientVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        l_meths = []
        l_attrs = []

        load_meths_attrs(l_meths, l_attrs, clsdict)

        for rec in ('accept', 'listen', 'socket'):
            if rec in l_meths:
                raise TypeError('В классе обнаружено использование запрещённого метода')

        super().__init__(clsname, bases, clsdict)

