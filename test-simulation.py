from modules.simulation import EvacuationSimulator

simulator = EvacuationSimulator()
print("Initial state:")
print(simulator.get_counts())


simulator.start_disaster(
    disaster_type="fire",
    affected_building="Block A"
)

print("\nFire detected!")
print(simulator.get_counts())
simulator.advance(10)

print("\nAfter 10 seconds:")
print(simulator.get_counts())
simulator.advance(10)

print("\nAfter 20 seconds:")
print(simulator.get_counts())
simulator.advance(10)

print("\nAfter 30 seconds:")
print(simulator.get_counts())