# Tab 1 Functions
import numpy as np

# Global Variables
# Dictionary of the prev round
undo_round = {
    "round":"1",
    "energy": "3",
    "base_energy": "3",
    "used": "0",
    "gained": "0",
    "destroyed": "0"
}

# Dictionary for the redo button
redo_round = {
    "round":"1",
    "energy": "3",
    "base_energy": "3",
    "used": "0",
    "gained": "0",
    "destroyed": "0"
}

# global current_base_energy
current_base_energy = "3"


class Tab1:
    # Private function to reset the values of the labels
    # of the rows of energy Used, Gained, and Destroyed
    def __reset_rows(canvas_arg, tab_tags_arg) -> None:
        canvas_arg.itemconfig(tab_tags_arg['used'], text = 0)
        canvas_arg.itemconfig(tab_tags_arg['gained'], text = 0)
        canvas_arg.itemconfig(tab_tags_arg['destroyed'], text = 0)
    

    # Private function for debugging
    def __print_base_energy(state_arg):
        global current_base_energy

        print("[{}]".format(state_arg))
        print("Undo Base Energy: {}".format(undo_round['base_energy']))
        print("Redo Base Energy: {}".format(redo_round['base_energy']))
        print("Current Base Energy: {}".format(current_base_energy))
        
    
    # Function to reset the entirety of Tab1
    def reset_app(canvas_arg, tab_tags_arg) -> None:
        global current_base_energy
        # Getting all the current values and saving it in
        # the redo_round dictionary for the redo function
        redo_round['round'] = canvas_arg.itemcget(tab_tags_arg['round'], 'text')
        redo_round['energy'] = canvas_arg.itemcget(tab_tags_arg['energy'], 'text')
        redo_round['used'] = canvas_arg.itemcget(tab_tags_arg['used'], 'text')
        redo_round['gained'] = canvas_arg.itemcget(tab_tags_arg['gained'], 'text')
        redo_round['destroyed'] = canvas_arg.itemcget(tab_tags_arg['destroyed'], 'text')

        # Resetting the round number and total energy labels
        canvas_arg.itemconfig(tab_tags_arg['round'], text = 1)
        canvas_arg.itemconfig(tab_tags_arg['energy'], text = 3)
        current_base_energy = 3

        # Calling the private function for resetting the
        # used, gained, and destroyed labels
        Tab1.__reset_rows(canvas_arg, tab_tags_arg)

        # Resetting the values of the undo_round dictionary
        undo_round["round"] = "1"
        undo_round["energy"] = "3"
        undo_round['used'] = "0"
        undo_round['gained'] = "0"
        undo_round['destroyed'] = "0"

        # Printing the base energy for every state for debugging
        Tab1.__print_base_energy("Reset")


    # Function that is called for the end turn button
    def end_turn(canvas_arg, tab_tags_arg) -> None:
        global current_base_energy

        # Getting the values of the round and total energy number
        round_num = int(canvas_arg.itemcget(tab_tags_arg['round'], 'text'))
        energy_num = int(canvas_arg.itemcget(tab_tags_arg['energy'], 'text'))

        # Saving the current state into the undo_round 
        # dictionary for the undo function
        undo_round["round"] = round_num
        undo_round["energy"] = energy_num
        undo_round['base_energy'] = current_base_energy
        undo_round['used'] = int(canvas_arg.itemcget(tab_tags_arg['used'], 'text'))
        undo_round['gained'] = int(canvas_arg.itemcget(tab_tags_arg['gained'], 'text'))
        undo_round['destroyed'] = int(canvas_arg.itemcget(tab_tags_arg['destroyed'], 'text'))

        # Adding 2 energy to the current total while clipping it
        # to a max value of 10 and a min value of 0.
        energy_num = np.clip((energy_num + 2), 0, 10)
        redo_round['base_energy'] = energy_num
        current_base_energy = redo_round['base_energy']

        # Adding 1 to the round counter, setting the new total value
        # and resetting the other rows to 0.
        canvas_arg.itemconfig(tab_tags_arg['round'], text = str(round_num+1))
        canvas_arg.itemconfig(tab_tags_arg['energy'], text = str(energy_num))
        Tab1.__reset_rows(canvas_arg, tab_tags_arg)

        # For debugging
        Tab1.__print_base_energy("End Turn")
    
    # Function to undo and return to the previous round state
    def undo(canvas_arg, tab_tags_arg) -> None:
        global current_base_energy

        if int(canvas_arg.itemcget(tab_tags_arg['round'], 'text')) != int(undo_round["round"]):
            redo_round['round'] = canvas_arg.itemcget(tab_tags_arg['round'], 'text')
            redo_round['energy'] = canvas_arg.itemcget(tab_tags_arg['energy'], 'text')
            redo_round['base_energy'] = current_base_energy
            redo_round['used'] = canvas_arg.itemcget(tab_tags_arg['used'], 'text')
            redo_round['gained'] = canvas_arg.itemcget(tab_tags_arg['gained'], 'text')
            redo_round['destroyed'] = canvas_arg.itemcget(tab_tags_arg['destroyed'], 'text')

            canvas_arg.itemconfig(tab_tags_arg['round'], text = undo_round["round"])
            canvas_arg.itemconfig(tab_tags_arg['energy'], text = undo_round["energy"])
            current_base_energy = undo_round['base_energy']

            canvas_arg.itemconfig(tab_tags_arg['used'], text = undo_round["used"])
            canvas_arg.itemconfig(tab_tags_arg['gained'], text = undo_round["gained"])
            canvas_arg.itemconfig(tab_tags_arg['destroyed'], text = undo_round["destroyed"])
            
            Tab1.__print_base_energy("Undo")

    
    # Function to redo and state before pressing the undo button
    def redo(canvas_arg, tab_tags_arg) -> None:
        global current_base_energy

        if int(canvas_arg.itemcget(tab_tags_arg['round'], 'text')) != int(redo_round["round"]):
            canvas_arg.itemconfig(tab_tags_arg['round'], text = redo_round["round"])
            canvas_arg.itemconfig(tab_tags_arg['energy'], text = redo_round["energy"])
            
            current_base_energy = redo_round['base_energy']

            canvas_arg.itemconfig(tab_tags_arg['used'], text = redo_round["used"])
            canvas_arg.itemconfig(tab_tags_arg['gained'], text = redo_round["gained"])
            canvas_arg.itemconfig(tab_tags_arg['destroyed'], text = redo_round["destroyed"])
            
            Tab1.__print_base_energy("Redo")


    def remove_energy(canvas_arg, tab_tags_arg, field_arg) -> None:
        energy_num = int(canvas_arg.itemcget(tab_tags_arg['energy'], 'text'))
        if energy_num-1 >= 0:
            used_num = int(canvas_arg.itemcget(field_arg, 'text'))
            canvas_arg.itemconfig(tab_tags_arg['energy'], text = str(energy_num - 1))
            canvas_arg.itemconfig(field_arg, text = str(used_num + 1))
    

    def return_energy(canvas_arg, tab_tags_arg, field_arg) -> None:
        used_num = int(canvas_arg.itemcget(field_arg, 'text'))
        if used_num-1 >= 0:
            energy_num = int(canvas_arg.itemcget(tab_tags_arg['energy'], 'text'))
            if energy_num < int(current_base_energy):
                canvas_arg.itemconfig(tab_tags_arg['energy'], text = str(energy_num + 1))
            canvas_arg.itemconfig(field_arg, text = str(used_num - 1))
    

    def add_energy(canvas_arg, tab_tags_arg, field_arg) -> None:
        energy_num = int(canvas_arg.itemcget(tab_tags_arg['energy'], 'text'))
        if energy_num < 10:
            gained_num = int(canvas_arg.itemcget(field_arg, 'text'))
            canvas_arg.itemconfig(field_arg, text = str(gained_num + 1))
            energy_num = np.clip((energy_num  + 1), 0, 10)
            canvas_arg.itemconfig(tab_tags_arg['energy'], text = str(energy_num))
    

    def remove_gained_energy(canvas_arg, tab_tags_arg, field_arg) -> None:
        gained_num = int(canvas_arg.itemcget(field_arg, 'text'))
        if gained_num - 1 >= 0:
            energy_num = int(canvas_arg.itemcget(tab_tags_arg['energy'], 'text'))
            if energy_num != int(current_base_energy):
                energy_num = np.clip((energy_num  - 1), 0, 10)
            canvas_arg.itemconfig(tab_tags_arg['energy'], text = str(energy_num))
            canvas_arg.itemconfig(field_arg, text = str(gained_num - 1))
