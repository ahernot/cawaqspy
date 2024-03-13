
def format_command_dict (command_dict: dict, indent_break_max = 0) -> str:
    """
    Recursively print the command dictionary in a human-readable format.

    Args:
        command_dict (dict): Command dictionary to print.
        indent_break_max (int): Maximum indentation level at which to print line breaks between elements (0 prints no breaks).
    
    Returns:
        str: Command file in string format
    """

    def __print_recur (
            subdict: dict,
            out_list: list = [],
            indent: int = 0,
            key_len_max: int = 0,
            indent_break_max: int = 0
        ) -> list:
        """
        _summary_

        Args:
            subdict (dict): Current subdict to print.
            out_list (list, optional): Current output list. Defaults to [].
            indent (int, optional): Current indent level. Defaults to 0.
            key_len_max (int, optional): Max key length for current subdict (for text formatting). Defaults to 0.
            indent_break_max (int, optional): Maximum indentation level at which to print line breaks between elements (0 prints no breaks). Defaults to 0.

        Returns:
            list: _description_
        """
        
        __types_single = (str, int, float, bool, type(None))
        __ichar = '\t'
        __iincr = 1

        def __serialize (x):
            if type(x) == bool:
                return 'YES' if x else 'NO'
            return x


        # Run through subdict's items
        for key, val in subdict.items():

            # Unpack subdicts
            if type(val) == dict:
                
                # Only one leaf (non-iterable value): compact writing (curly brackets on the same line)
                subitems = list(val.values())
                if len(subitems) == 1 and type(subitems[0]) in __types_single:
                    print_prefix = f'{__serialize(key)} '
                    print_suffix = f'= {{ {__serialize(list(val.keys())[0])} }}'
                    if key_len_max > len(print_prefix): print_prefix += ' ' * (key_len_max - len(print_prefix))
                    out_list.append (__ichar*indent + print_prefix + print_suffix)  # Print
                
                # Multiple subitems: expanded dict writing (recursive call) - no formatting adjustment with spaces
                else:
                    # Calculate key_len_max (ignore keys of expanded dicts and special keys)
                    keys_eligible_ = list()
                    for key_, val_ in val.items():
                        # Special keys
                        if key_ == '__inline__': continue
                        # Non-iterable values
                        if type(val_) in __types_single:
                            keys_eligible_.append(key_)
                        # Single-element dict values
                        elif type(val_) == dict:
                            subitems = list(val_.values())
                            if len(subitems) == 1 and type(subitems[0]) in __types_single:
                                keys_eligible_.append(key_)
                    key_len_max_ = max([len(key) for key in keys_eligible_]) + 1 if keys_eligible_ else 0

                    out_list.append (__ichar*indent + f'{__serialize(key)} = {{')
                    out_list = __print_recur(val, out_list=out_list, indent=indent+__iincr, key_len_max=key_len_max_)
                    out_list.append (__ichar*indent + '}')


            # Unpack lists to assign the key to each subdictionary
            elif type(val) == list:
                # List contains only non-iterable elements (only print key once)
                if all((type(v) in __types_single  for v in val)):
                    print_prefix = f'{__serialize(key)} '
                    out_list.append (__ichar*indent + print_prefix + f'= {val[0]}')
                    for item in val[1:]:
                        out_list.append (__ichar*indent + ' '*len(print_prefix) + f'= {item}')

                # List contains dictionary elements
                else:
                    for item in val:
                        out_list = __print_recur({key: item}, out_list=out_list, indent=indent)  # Distribute print_recur across all subdicts contained in the list


            # End node (leaf)
            else:
                # Inline text (prints value only, formatted as "value") for elements of dict with '__inline__' key
                if key == '__inline__':
                    out_list.append (__ichar*indent + __serialize(val))

                # Regular key-pair formatted as "key = value"
                else:
                    print_prefix = f'{__serialize(key)} '
                    print_suffix = f'= {__serialize(val)}'
                    if key_len_max > len(print_prefix): print_prefix += ' ' * (key_len_max - len(print_prefix))
                    out_list.append (__ichar*indent + print_prefix + print_suffix )
            

            # Line break between main sections
            if indent < indent_break_max:
                out_list.append ('')

        return out_list
    
    return '\n'.join( __print_recur(command_dict, out_list=[], indent=0, key_len_max=0, indent_break_max=indent_break_max) )
