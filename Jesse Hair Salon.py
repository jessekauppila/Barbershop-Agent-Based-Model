import mesa
import random


class Barber(mesa.Agent):
    """An agent with availability or not"""

    def __init__(self, unique_id, model, customer=None):
        super().__init__(unique_id, model)
        # Create the Barber's current_hair_cut_length variable and set the initial values.
        self.current_hair_cut_length = 0
        self.my_customer = customer

    def step(self):
        # Who's hair is the barber cutting:

        if self.my_customer is not None:
            print(
                f"Barber {str(self.unique_id)}, hair cut left: {str(self.current_hair_cut_length)}")
            print(f" Cutting customer: {str(self.my_customer)}")
        # else:
        #     print (f"Barber {str(self.unique_id)} available!")

        if self.current_hair_cut_length > 0:
            self.current_hair_cut_length -= 1


class Customer(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.time_waiting = 0
        self.marked_as_waiting = True
        self.marked_as_getting_haircut = False
        self.marked_as_finished_haircut = False
        self.marked_as_left_angry = False
        self.current_hair_cut_length = 0
        self.my_barber = None

    def step(self):

        self.mark_as_waiting()
        self.customer_leaves()
        self.finishing_haircut()
        self.time_waiting += 1
    def mark_as_waiting(self):
        if self.marked_as_getting_haircut:
            self.marked_as_waiting = False
            print(
                f"Customer {str(self.unique_id)} getting cut for {str(self.current_hair_cut_length)} minutes with Barber {str(self.my_barber)}.")
    def customer_leaves(self):
        if self.marked_as_waiting is True:
            print(f"Customer {str(self.unique_id)} waited {str(self.time_waiting)} minutes.")
        if self.time_waiting > 5 and self.marked_as_waiting is True:
            print(f"Customer {str(self.unique_id)} ANGRY, leaves and removed.")
            self.marked_as_left_angry = True
            self.remove()

    def finishing_haircut(self):
        if self.current_hair_cut_length == 0 and self.marked_as_getting_haircut == True:
            self.marked_as_finished_haircut = True
            self.remove()

            print(f"Customer {str(self.unique_id)} FINISHED with Barber {str(self.my_barber)} and removed")
            for agent in self.model.schedule.agents:
                if isinstance(agent, Barber) and agent.my_customer == self.unique_id:
                    agent.my_customer = None
        else:
            self.current_hair_cut_length -= 1

class Barbesrhop_Model(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, num_Barber):
        super().__init__()
        self.schedule = mesa.time.RandomActivation(self)
        self.time = 0
        self.customer_count = 0

        # Create Barber
        self.num_Barber = num_Barber
        for i in range(self.num_Barber):
            a = Barber(i, self, None)
            # Add the agent to the scheduler
            self.schedule.add(a)

        # Initialize the longest waiting customer and their waiting time
        self.longest_waiting_customer_num = 1
        self.longest_waiting_time = 0

    def step(self):
        """Advance the model by one step."""
        self.create_customer()
        self.assign_customer_to_barber()
        self.find_longest_waiting_customer()
        self.time += 1  # Increment time

        self.schedule.step()

    def find_longest_waiting_customer(self):

        # Find the customer with the longest waiting time
        for agent in self.schedule.agents:
            if isinstance(agent,
                          Customer) and agent.time_waiting > self.longest_waiting_time and agent.marked_as_waiting is True:
                self.longest_waiting_customer_num = agent.unique_id
                self.longest_waiting_time = agent.time_waiting
                print(
                    f"Longest waiting customer {self.longest_waiting_customer_num} with {self.longest_waiting_time} minutes wait.")

    def assign_customer_to_barber(self):
        # Assign the longest waiting customer to a barber
        for agent in self.schedule.agents:
            if isinstance(agent, Barber) and agent.my_customer is None:
                # print(f"Barber {agent.unique_id} is available!")
                for customer_longest_waiting in self.schedule.agents:
                    if (isinstance(customer_longest_waiting,
                                   Customer) and customer_longest_waiting.unique_id == self.longest_waiting_customer_num
                            and customer_longest_waiting.marked_as_waiting):
                        agent.my_customer = self.longest_waiting_customer_num
                        print(f" Customer {agent.my_customer} assigned to Barber {agent.unique_id}")
                        starting_hair_cut_length = 2  # create length of time of haircut
                        agent.current_hair_cut_length = starting_hair_cut_length
                        customer_longest_waiting.current_hair_cut_length = starting_hair_cut_length
                        customer_longest_waiting.marked_as_waiting = False
                        customer_longest_waiting.marked_as_getting_haircut = True
                        customer_longest_waiting.my_barber = agent.unique_id
                        break
    def create_customer(self):
        if self.time % 3 == 0:
            customer = Customer(self.customer_count, self)  # Create a new customer with a unique ID
            self.customer_count += 1  # Increment the customer count for the next customer
            self.schedule.add(customer)  # Add the customer to the scheduler


model = Barbesrhop_Model(1)
for i in range(20):
    model.step()
