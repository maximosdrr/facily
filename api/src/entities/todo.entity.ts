import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class Todo {
  @PrimaryGeneratedColumn('uuid')
  id?: string;

  @Column()
  type: string;

  @Column()
  index: number;
}
