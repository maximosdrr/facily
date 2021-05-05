import { Module } from '@nestjs/common';
import { UserService } from './user.service';
import { UserController } from './user.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from 'src/entities/user.entity';

@Module({
  providers: [UserService],
  controllers: [UserController],
  exports: [UserModule],
  imports: [TypeOrmModule.forFeature([User])],
})
export class UserModule {}
