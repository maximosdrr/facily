import {
  BadRequestException,
  Injectable,
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { User } from 'src/entities/user.entity';
import { Repository } from 'typeorm';

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User) private readonly userRepo: Repository<User>,
  ) {}

  async create(user: User) {
    const emailAlreadyExists = await this.emailAlreadyExists(user);

    if (!emailAlreadyExists)
      throw new BadRequestException('Esse email já está cadastrado');

    return await this.userRepo.save(user);
  }

  async loginWithEmailAndPassword({ email, password }) {
    const user = await this.userRepo.findOne({ where: { email, password } });

    if (!user) throw new NotFoundException('Esse usuario não existe');

    return user;
  }

  async delete(id: string) {
    return this.userRepo.delete(id);
  }

  async update(user: User) {
    const userToUpdate = await this.userRepo.findOne(user.id);

    if (!userToUpdate) throw new NotFoundException('Esse usuario não existe');

    userToUpdate.email = user.email;
    userToUpdate.password = user.password;

    return this.userRepo.save(userToUpdate);
  }

  private async emailAlreadyExists({ email }) {
    try {
      const user = this.userRepo.findOne({ where: { email } });
      if (user) return true;

      return false;
    } catch (e) {
      throw new InternalServerErrorException(
        'Não foi possivel verificar se esse usuario já exisita, um erro interno no servidor está impedindo isso',
      );
    }
  }
}
