// Entity Template
// Use for domain objects with identity

export abstract class Entity<T> {
  protected abstract id: T;
  
  equals(other: Entity<T>): boolean {
    return this.id === other.id;
  }
}

export class User extends Entity<UserId> {
  private _id: UserId;
  private _email: Email;
  private _name: string;
  
  get id(): UserId {
    return this._id;
  }
  
  get email(): Email {
    return this._email;
  }
  
  get name(): string {
    return this._name;
  }
  
  // Behavior, not just setters
  changeEmail(newEmail: Email): void {
    this._email = newEmail;
  }
  
  changeName(newName: string): void {
    if (!newName || newName.length < 2) {
      throw new DomainError("Name must have at least 2 characters");
    }
    this._name = newName;
  }
}