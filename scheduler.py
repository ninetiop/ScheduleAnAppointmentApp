from datetime import datetime, timedelta

DELTA_SHIFT_BETWEEN_APPOINTMENT = timedelta(minutes=30)

class Scheduler:
    def __init__(self, rows_appointments) -> None:
        self._busy_slot = self._get_busy_slot(rows_appointments)

    def difference_minutes(self, date, date2):
        diff = date - date2
        diff_in_min = diff.total_seconds() // 60
        return abs(diff_in_min)
    
    def is_delta_superior(self, date, min_date, max_date):
        ret = False
        if date < min_date:
            if self.difference_minutes(date, min_date) >= 30:
                ret = True 
        if date > min_date and date < max_date:
            if self.difference_minutes(min_date, date) >= 30:
                if self.difference_minutes(date, max_date) >= 30:
                    ret = True
        if date > max_date:
            if self.difference_minutes(max_date, date) >= 30:
                ret = True
        return ret

    def is_in_range(self, date, min_date, max_date):
        ret = False
        if date > min_date and date < max_date:
            return True
        return ret
    
    def check_slot_available(self, slot_available):
        if len(slot_available) == 1:
            if slot_available[0] is True:
                return True
        if len(slot_available) == 2:
            if slot_available[1] is True:
                return True
        if len(slot_available) > 2:
            # Find the index of the first True value
            first_true_index = slot_available.index(True)
            # Check if all elements after the first True are True
            all_true = all(slot_available[i] for i in range(first_true_index + 1, len(slot_available)))
            return all_true
        return False


    def get_full_day_available_slot(self, day):
        full_day_available_slot = []
        for hour in range(8, 20):
            for min in ['00', '15', '30', '45']:
                if hour < 10:
                    h = '0' + str(hour)
                else:
                    h = str(hour)
                slot = day
                slot += ' '
                slot += h 
                slot += ':' 
                slot += str(min)
                slot += ':00'
                slot = datetime.strptime(slot, "%Y-%m-%d %H:%M:%S")
                size_busy_slot = len(self._busy_slot)
                if size_busy_slot == 0:
                    full_day_available_slot.append(slot)
                if size_busy_slot == 1:
                    for b_slot in self._busy_slot:
                        if self.difference_minutes(b_slot, slot) >= 30:
                            full_day_available_slot.append(slot)
                if size_busy_slot > 1:
                    i = 0
                    slot_available = []
                    while i < size_busy_slot - 1:
                        if self._busy_slot[i] == slot:
                            break
                        range_min_date = self._busy_slot[i]
                        range_max_date = self._busy_slot[i+1]
                        if self.is_delta_superior(slot, range_min_date, range_max_date):
                            slot_available.append(True)
                        else:
                            if self.is_in_range(slot, range_min_date, range_max_date):
                                break
                            slot_available.append(False)
                        i += 1
                    if self.check_slot_available(slot_available) and i == size_busy_slot - 1:
                        full_day_available_slot.append(slot)                              
        return full_day_available_slot

    def _get_busy_slot(self, rows_appointments):
        busy_slot = []
        if len(rows_appointments) > 0:
            for row in rows_appointments:
                date = row[3]
                busy_slot.append(date)
            busy_slot = sorted(busy_slot)
        return busy_slot