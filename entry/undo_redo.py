import copy
from collections import deque


class ActionStack():
    def __init__(self, root):
        self.undo_stack = deque()
        self.redo_stack = deque()
        self.root = root

    def add_undo(self, origin, restore_data=None):
        action = {'origin': origin}
        if restore_data is not None:
            restore_object = {'restore': restore_data}
        else:
            restore_object = {'restore': None}
        action.update(restore_object)
        self.undo_stack.append(action)
        self.overflow()

    def clear_all(self):
        self.undo_stack.clear()
        self.redo_stack.clear()

    def clear_redo(self):
        self.redo_stack.clear()

    def undo_empty(self):
        return len(self.undo_stack) == 0

    def redo_empty(self):
        return len(self.redo_stack) == 0

    def undo(self):
        if len(self.undo_stack) > 0:
            back_action = self.undo_stack.pop()
            if isinstance(back_action['restore'], list):
                old_token_list = copy.deepcopy(self.root.token_list)
                redo_data = {
                    'origin': 'list',
                    'restore': old_token_list
                }
                self.redo_stack.append(redo_data)
                self.overflow()
                return back_action
            else:
                self.redo_stack.append(back_action)
                self.overflow()
                return back_action
        else:
            return None

    def redo(self):
        if len(self.redo_stack) > 0:
            fwd_action = self.redo_stack.pop()
            if isinstance(fwd_action['restore'], list):
                old_token_list = copy.deepcopy(self.root.token_list)
                undo_data = {
                    'origin': 'list',
                    'restore': old_token_list
                }
                self.undo_stack.append(undo_data)
                self.overflow()
                return fwd_action
            else:
                self.undo_stack.append(fwd_action)
                self.overflow()
                return fwd_action
        else:
            return None

    def overflow(self):
        if len(self.undo_stack) > 10:
            self.undo_stack.popleft()
        if len(self.redo_stack) > 10:
            self.redo_stack.popleft()

    def peek(self, stack):
        if stack == 'undo':
            if len(self.undo_stack) > 1:
                return self.undo_stack[-1]['origin']
            else:
                return None

        if stack == 'redo':
            if len(self.redo_stack) > 1:
                return self.redo_stack[-1]['origin']
            else:
                return None