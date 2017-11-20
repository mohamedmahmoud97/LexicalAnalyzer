def visualize(nfa, start, end, verbose=False):
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import xdot
    window = xdot.DotWindow()
    dotcode = 'digraph G {\n'
    for node in nfa.keys():
        if node == start:
            dotcode += str(node) + " [shape=box, style=filled, color=red];\n"
        if node in end:
            dotcode += str(node) + " [peripheries=2];\n"
        for node2,transition in nfa[node]:
            dotcode += str(node) + "->" + str(node2) + " [label=\"" + str(transition) + "\"];\n"
    dotcode += '}'
    if verbose:
        print(dotcode)
    window.set_dotcode(dotcode)
    window.connect('delete-event', Gtk.main_quit)
    Gtk.main()

